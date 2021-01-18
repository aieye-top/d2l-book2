# D2L-Book2: A Toolkit for Hands-on Books

This package helps you build and publish **a book with Python code**, or
**Python package documents with tutorials**. The document site is available at
docs/

TODO: https://github.com/d2l-ai/d2l-book/commit/5f078f8812bb0f2bf45d9648fa80e1ba63f7b524
https://github.com/d2l-ai/d2l-book/commit/5f078f8812bb0f2bf45d9648fa80e1ba63f7b524



Install:

```bash
pip install git+https://github.com/aieye-top/d2l-book2/
```

https://book.d2l.ai/user/deploy.html



## To deploy to Github

The only difference is

```bash
d2lbook2 deploy html
```

instead of `d2lbook deploy html`

 For this example, the URL is https://github.com/aieye-top/d2cl

The result:
https://aieye-top.github.io/d2cl/

## Docker

 https://github.com/ykxVK8yL5L/6pan/blob/main/.github/workflows/docker-image.yml
 https://www.youtube.com/watch?v=fSKbUgRL3vA

### Not China:

```bash
docker pull stevenjokes/d2l-book2:latest
```

```bash
docker run stevenjokes/d2l-book2:latest build html
```

---

### 国内：

```bash
docker pull registry.cn-shanghai.aliyuncs.com/csq-dl/d2l-book2:latest
```

#### 用例：

(base) PS C:\Users\a8679> docker run registry.cn-shanghai.aliyuncs.com/csq-dl/d2l-book2:latest
usage: d2lbook2 [-h] {build,deploy,clear,activate,translate}

D2L Book: Publish a book based on Jupyter notebooks. Run d2lbook2 command -h
to get the help message for each command.

positional arguments:
  {build,deploy,clear,activate,translate}

optional arguments:
  -h, --help            show this help message and exit



```bash
docker run -dit -v D:/onedrive/Documents/read/d2cl-whole/d2cl/d2cl:/share registry.cn-shanghai.aliyuncs.com/csq-dl/d2l-book2:latest /bin/bash
```

--rm:在容器终止运行后自动删除容器文件
-d: 后台运行容器，并返回容器ID；
-i: 以交互模式运行容器，通常与 -t 同时使用；
-t: 为容器重新分配一个伪输入终端，通常与 -i 同时使用；
-v: 把宿主机的/d/onedrive/Documents/read/d2cl-whole/d2cl/d2cl下载目录挂载到registry.cn-shanghai.aliyuncs.com/csq-dl/d2l-book2:latest容器的/share目录下。


```bash
docker ps
docker exec -it <container_id> /bin/bash
```

把CONTAINER ID粘贴到<container_id>位置

```bash
cd ..
ls
d2lbook2 build html
```

