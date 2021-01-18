FROM ubuntu:20.04

RUN apt update && apt dist-upgrade -y && DEBIAN_FRONTEND=noninteractive apt install -y python3-pip pandoc librsvg2-bin git latexmk texlive-xetex texlive-fonts-extra && apt clean

RUN pip3 install git+ssh://git@github.com:aieye-top/d2l-book2.git#egg=d2lbook2

WORKDIR /d2lbook2

CMD ["d2lbook2", "--help"]
