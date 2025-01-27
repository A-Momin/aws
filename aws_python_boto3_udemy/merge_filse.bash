cd sec06*
f=$(ls -L *.py)


for file in $f
do
    # echo "<!-- ===================================================================== -->" >> 00.all.md
    echo "### $file" >> 00.all.md
    # echo "<!-- ===================================================================== -->" >> 00.all.md
    echo -e "\n" >> 00.all.md
    echo -e "\`\`\`python" >> 00.all.md

    cat $file >> 00.all.md
    # echo -e "\n" >> 00.all.md
    echo -e "\n\`\`\`" >> 00.all.md
    echo -e "\n" >> 00.all.md
    

    # echo $file
done

cd ..