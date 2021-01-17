FROM ubuntu:20.04

RUN apt update && apt dist-upgrade -y && DEBIAN_FRONTEND=noninteractive apt install -y python3-pip pandoc librsvg2-bin git latexmk texlive-xetex texlive-fonts-extra && apt clean

RUN pip install git+https://github.com/aieye-top/d2l-book2/tree/master/d2lbook2

WORKDIR /book

CMD ["d2lbook2", "--help"]