############################################
#
############################################
# Get current dir
currentDir=$(pwd)
VIRTUAL_ENV=${currentDir}/venv
# Activate the virtual environment
if [[ -d "${VIRTUAL_ENV}" ]]; then
  source "${VIRTUAL_ENV}/bin/activate"
fi
############################################
urlToDL=${1}
additionalArgs=${2=""}
epoch_time=$(date +%s)
# For debug
urlFirstChars=${urlToDL:0:8}
urlLastChars=${urlToDL: -16}
# Make the output folder
if [[ ! -d "${currentDir}/output" ]]; then
  mkdir -p "${currentDir}/output"
fi
# print debug
cd "${currentDir}/output"
echo "******************"
echo "Downloading '${urlFirstChars}...${urlLastChars}'"
echo "Resulting file will be: video_[TITLE]_${epoch_time}.[EXT]"
echo "******************"
echo "Summoning helper..."
videoURI=$(python "${currentDir}/helper.py" -u "${urlToDL}")
echo "Calling youtube-dl..."
# execute the download
yt-dlp ${additionalArgs} --print-traffic --output "video_%(title)s_${epoch_time}.%(ext)s" --external-downloader aria2c --external-downloader-args "-c --max-concurrent-downloads=5 --max-connection-per-server=10" "${videoURI}"
rm -rf *.part*
echo "******************"
echo "Done."
echo "******************"
cd "${currentDir}"
############################################
# Deactivate the virtual environment
if [[ -d "${VIRTUAL_ENV}" ]]; then
  deactivate
fi
############################################