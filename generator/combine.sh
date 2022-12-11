cd meshbaker

INPUT=$1

# if INPUT is empty, set to 0
if [ -z "$INPUT" ]; then
  INPUT="0"
fi

npm run atlas -- ../out/$INPUT.glb ../combined/$INPUT.glb