#!/bin/bash

# Create the assets/pdf directory if it doesn't exist
mkdir -p assets/pdf
mkdir -p temp

# Get the current date
CURRENT_DATE=$(date +%Y-%m-%d)

# Loop through all Markdown files in the docs directory
for file in docs/*.md; do
    filename=$(basename -- "$file")
    name="${filename%.*}" # Extract file name without extension
    cp "$file" "temp/${name}_temp.md"
    header_file="temp/${name}_header.tex"
    number_sections=""

    # Enable section prefixing for documents that request it
    if grep -q '^section_prefix:' "$file"; then
        number_sections="--number-sections"
        cat > "$header_file" <<'EOF'
\usepackage{enumitem}
\renewcommand{\thesection}{\S\arabic{section}}
\renewcommand{\thesubsection}{\arabic{section}.\arabic{subsection}}
\renewcommand{\thesubsubsection}{\arabic{section}.\arabic{subsection}.\arabic{subsubsection}}
\makeatletter
\renewcommand{\@seccntformat}[1]{\ifcsname the#1\endcsname\csname the#1\endcsname\hspace{0.4em}\fi}
\renewcommand{\numberline}[1]{#1\hspace{0.6em}}
\makeatother
EOF
    else
        echo "\\usepackage{enumitem}" > "$header_file"
    fi
    
    # Replace date placeholder in Markdown content
    sed -i "s/{{ site.time | date: \"%d-%m-%Y\" }}/$CURRENT_DATE/g" "temp/${name}_temp.md"
    
    # Replace date in the metadata block
    sed -i "s/date: {{ site.time | date: \"%d-%m-%Y\" }}/date: $CURRENT_DATE/g" "temp/${name}_temp.md"

    # Replace TOC syntax for LaTeX
    sed -i '/^\* TOC$/{N;s|.*\n.*$|\\clearpage\\renewcommand{\\contentsname}{Inhaltsverzeichnis}\n\\tableofcontents\n\\clearpage|}' "temp/${name}_temp.md"
    
    # Remove HTML-only blocks for PDF generation
    sed -i '/<div class="html-only"/,/^<\/div>$/d' "temp/${name}_temp.md"

    # Convert HTML ordered lists (type="a") to LaTeX enumerate with alphabetic labels
    sed -i '
    s|<ol type="a">|\\begin{enumerate}[label=\\alph*.]|g;
    s|</ol>|\\end{enumerate}|g;
    s|<li>|\\item |g;
    s|</li>||g;
    ' "temp/${name}_temp.md"
    
    # Convert Markdown to PDF
    pandoc "temp/${name}_temp.md" -o "assets/pdf/${name}.pdf" \
      $number_sections \
      --toc-depth=2 \
      --pdf-engine=xelatex \
      -V geometry:margin=1in \
      --include-in-header="$header_file" \
      --resource-path=./docs
done

echo "PDFs successfully generated in assets/pdf/"
