FROM texlive/texlive:latest

RUN apt-get update && apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        python3-requests \
        make \
        git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /workspace

CMD ["latexmk", "-pdf", "-bibtex", "-interaction=nonstopmode", "-halt-on-error", "cycles_refuted.tex"]
