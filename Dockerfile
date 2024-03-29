FROM ubuntu:latest

RUN mkdir -p /home/ePortalService
WORKDIR /home/ePortalService

COPY requirements.txt /home/ePortalService

RUN apt update && apt dist-upgrade -y && DEBIAN_FRONTEND=noninteractive apt install -y python3-pip pandoc librsvg2-bin git latexmk texlive-lang-cjk texlive-xetex texlive-fonts-extra && apt clean

RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install -U git+https://github.com/aieye-top/d2l-book2#egg=d2lbook2

RUN python3 -m pip install --upgrade -r requirements.txt
WORKDIR /d2lbook2

CMD ["d2lbook2", "-h"]
