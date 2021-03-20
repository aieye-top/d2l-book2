import os
import glob
import shutil
import logging

def rm_ext(filename):
    return os.path.splitext(filename)[0]

def find_files(pattern, root=None, excluded_pattern=None):
    fnames = []
    patterns = pattern.split()
    for p in patterns:
        if root is not None:
            p = os.path.join(root, p)
        if os.path.isdir(p):
            p = os.path.join(p, '**')
        for fn in glob.glob(p, recursive=True):
            if os.path.isfile(fn):
                fnames.append(fn)
    if not excluded_pattern:
        return fnames
    excluded_fnames = find_files(excluded_pattern, root)
    return [fn for fn in fnames if fn not in excluded_fnames]

def get_mtimes(fnames):
    if isinstance(fnames, str):
        return os.path.getmtime(fnames)
    return [os.path.getmtime(fn) for fn in fnames]

def split_fname(fname, base_dir, ext=None):
    fname = os.path.relpath(fname, base_dir)
    base, fext = os.path.splitext(fname)
    if fext.startswith('.'):
        fext = fext[1:]
    if ext and ext != fext:
        logging.warn("%s doesn't have extension %s", fname, ext)
    return base, fext

def get_tgt_fname(src_dir, src_fname, tgt_dir, src_ext, tgt_ext):
    fname, ext = split_fname(src_fname, src_dir, src_ext)
    if tgt_ext:
        ext = tgt_ext
    return os.path.join(tgt_dir, fname+'.'+ext)

def get_updated_files(src_fnames, src_dir, tgt_dir,
                      src_ext=None, tgt_ext=None, deps_mtime=0):
    updated_fnames = []
    for src_fn in src_fnames:
        tgt_fn = get_tgt_fname(src_dir, src_fn, tgt_dir, src_ext, tgt_ext)
        if (not os.path.exists(tgt_fn) # new
            or get_mtimes(src_fn) > get_mtimes(tgt_fn) # target is old
            or get_mtimes(tgt_fn) < deps_mtime): # deps is updated
            updated_fnames.append((src_fn, tgt_fn))
    return list(set(updated_fnames))


def get_tgt_files_from_src_pattern(pattern, tgt_dir, src_ext, tgt_ext):
    """Get files with tgt_ext in tgt_dir according to pattern with src_ext"""
    patterns = pattern.split()
    for i, p in enumerate(patterns):
        f, ext = os.path.splitext(p)
        if src_ext and ext == '.' + src_ext and tgt_ext:
            patterns[i] = f + '.' + tgt_ext
    return find_files(' '.join(patterns), tgt_dir)


def get_files_to_rm(pattern, src_dir, tgt_dir, src_ext=None, tgt_ext=None):
    """Return files under tgt_dir whose corresponding src file is removed under src_dir."""
    tgt_files = get_tgt_files_from_src_pattern(pattern, tgt_dir, src_ext, tgt_ext)
    to_removes = []
    for tgt_fn in tgt_files:
        # If tgt_ext is provided, only files with tgt_ext in tgt_dir are
        # considered being removed. Note that ipynb to rst may generate svg
        # files, which should not be removed though these svg files do not have
        # corresponding files in src_dir
        if tgt_ext:
            fext = os.path.splitext(tgt_fn)[1]
            if fext.startswith('.'):
                fext = fext[1:]
            if tgt_ext != fext:
                continue
        # By switching args, it actually get_src_fname.
        src_fn = get_tgt_fname(tgt_dir, tgt_fn, src_dir, tgt_ext, src_ext)
        if not os.path.exists(src_fn):
            to_removes.append(tgt_fn)
    return to_removes


def rm_empty_dir(path, rmed_empty_dirs):
    """Recursively remove empty directories under and including path."""
    if not os.path.isdir(path):
        return

    fnames = os.listdir(path)
    if len(fnames) > 0:
        for fn in fnames:
            fpath = os.path.join(path, fn)
            if os.path.isdir(fpath):
                rm_empty_dir(fpath, rmed_empty_dirs)

    if len(os.listdir(path)) == 0:
        rmed_empty_dirs.append(str(path))
        os.rmdir(path)

def hide_individual_data_files(fns):
    """To display concisely: _build/eval/data/A/B/C/D -> _build/eval/data/A."""
    concise_fns = set()
    for fn in fns:
        concise_fn = []
        fn_components = fn.split('/')
        i = 0
        seen_data = False
        while i < len(fn_components) and not seen_data:
            component = fn_components[i]
            concise_fn.append(component)
            if component == 'data':
                seen_data = True
            i += 1
        if i < len(fn_components) - 1:
            next_component = fn_components[i + 1]
            if next_component.isdigit():
                concise_fn.append('<some digit>')
            else:
                concise_fn.append(next_component)
            if i < len(fn_components) - 2:
                concise_fn.append('')  # For indicating dir instead of file
        concise_fns.add('/'.join(concise_fn))
    return concise_fns

def mkdir(dirname):
    os.makedirs(dirname, exist_ok=True)


def copy(src, tgt):
    mkdir(os.path.dirname(tgt))
    shutil.copy(src, tgt)

# https://blog.csdn.net/qq_44107838/article/details/103139126
def copy_dir(src,tgt):

    '''将一个目录下的全部文件和目录,完整地<拷贝并覆盖>到另一个目录'''
    # src 源目录
    # tgt 目标目录

    if not (os.path.isdir(src) and os.path.isdir(tgt)):
        # 如果传进来的不是目录
        # print("传入目录不存在")
        return

    for a in os.walk(src):
        #递归创建目录
        for d in a[1]:
            dir_path = os.path.join(a[0].replace(src,tgt),d)
            if not os.path.isdir(dir_path):
                os.makedirs(dir_path)
        #递归拷贝文件
        for f in a[2]:
            dep_path = os.path.join(a[0],f)
            arr_path = os.path.join(a[0].replace(src,tgt),f)
            shutil.copy(dep_path,arr_path)

def get_time_diff(tik, tok):
    h, remainder = divmod((tok - tik).seconds, 3600)
    m, s = divmod(remainder, 60)
    return "%02d:%02d:%02d" % (h, m, s)

def run_cmd(cmd, verbose=False):
    if isinstance(cmd, str):
        cmd = [cmd]
    cmd = ' '.join(cmd)
    if verbose:
        logging.info('Run "%s"', cmd)
    ret = os.system(cmd)
    if ret != 0:
        exit(-1)

def split_config_str(config_str, num_items_per_line=None):
    items = []
    if not config_str:
        return items
    lines = config_str.split('\n')
    for i, line in enumerate(lines):
        items.append([tk.strip() for tk in line.split(',') if tk.strip()])
        if num_items_per_line and len(items[-1]) != num_items_per_line:
            logging.fatal("The items in %d-th line (%d) doesn't"
                          " match the required (%d)"%(i, len(items[-1]), num_items_per_line))
            logging.fatal("The raw string is:\n"+config_str)
    return items
