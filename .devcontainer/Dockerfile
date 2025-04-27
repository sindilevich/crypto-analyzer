FROM python:3-slim-bookworm

# Set custom bash prompt
RUN echo 'export PS1="\[\033[0;32m\]\u\[\033[0m\] \[\342\236\234\] \[\033[1;34m\]\w\[\033[0m\] \[\033[0;36m\](\[\033[1;31m\]\$(git rev-parse --abbrev-ref HEAD 2>/dev/null)\[\033[0;36m\]) \[\033[0m\]\$ "' >> /root/.bashrc

RUN apt-get update \
	&& apt-get install -y curl \
	&& apt-get install -y git \
	&& apt-get install -y jq \
	&& apt-get install -y sudo \
	&& apt-get install -y wget

ENV PATH="${PATH}:/root/.local/bin"