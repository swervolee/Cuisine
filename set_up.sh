#!/bin/bash
# Compiles and sets up server to serve static content

# Get current timestamp
timestamp=$(date +"%Y%m%d%H%M%S")

# Create the tar file
tar_file="versions/web_static_$timestamp.tgz"
tar -czvf "$tar_file" ./web_static/

# Extract the filename
file_n=$(basename "$tar_file")

# Print the filename
echo "$file_n is the filename"

# Remove the extension
no_ext="${file_n%.*}"

# Print the filename without extension
echo "$no_ext"

path="/data/cuisine_static/releases"

# Create directory for extracted contents
mkdir -p "$path/$no_ext"

# Extract contents
tar -xvzf "$tar_file" -C "$path/$no_ext/"

# Cleanup temporary files
rm -f "$tar_file"

# Move extracted files to proper location
mv "$path/$no_ext/web_static/"* "$path/$no_ext/"

# Remove unnecessary directory
rm -rf "$path/$no_ext/web_static"

# Remove the compressed file in /tmp
rm -rf /tmp/"$file_n"

# Check if symbolic link exists and remove if it does
if [ -L "/data/web_static/current" ]; then
    echo "Deleting current symbolic link"
    rm -rf /data/web_static/current
fi

# Create symbolic link
ln -s "$path/$no_ext" /data/cuisine_static/current
