# bash script to convert all png files in a directory to jpg and resize them

cd blend/textures

echo 'Converting png to jpg'
for f in *.png; do
    echo "Processing $f file..."
    # take action on each file. $f store current file name
    convert "$f" "${f%.*}.jpg"
done

echo 'Moving jpg files to appropriate folders'
for f in *.jpg; do
    echo "Processing $f file..."
    # take action on each file. $f store current file name
    if [[ $f == *"emissive"* ]] || [[ $f == *"Image_3"* ]] || [[ $f == *"Emiss"* ]]; then
        echo "Resizing $f to 1024x1024"
        convert "$f" -resize 1024x1024 "$f"
    elif [[ $f == *"diffuse"* ]] || [[ $f == *"Color"* ]] || [[ $f == *"Image_0"* ]] || [[ $f == *"baseColor"* ]]; then
        echo "Resizing $f to 2048x2048"
        convert "$f" -resize 2048x2048 "$f"
    elif [[ $f == *"norm"* ]] || [[ $f == *"Image_2"* ]] || [[ $f == *"NM"* ]]; then
        echo "Resizing $f to 2048x2048"
        convert "$f" -resize 2048x2048 "$f"
    elif [[ $f == *"roug"* ]] || [[ $f == *"Image_1"* ]] || [[ $f == *"Roug"* ]] || [[ $f == *"metallic"* ]] || [[ $f == *"occlusion"* ]]; then
        echo "Resizing $f to 1024x1024"
        convert "$f" -resize 1024x1024 "$f"
    fi
done