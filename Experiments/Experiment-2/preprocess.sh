ls data/Devnagri-Family/* | grep -v .en$ | xargs cat > data/data.devnagri
ls data/Devnagri-Family/* | grep en$ | xargs cat > data/data.en
