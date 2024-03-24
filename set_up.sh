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
echo "$file_n"

# Remove the extension
no_ext="${file_n%.*}"

# Print the filename without extension
echo "$no_ext"

path="/data/cuisine_static/releases/"

cp "$tar_file" /tmp
mkdir -p "$path$no_ext"
tar -xzf /tmp/"$file_n" -C "$path/$no_ext"
mv "$path/$no_ext/web_static/*" "$path/$no_ext"
rm -rf "$path/$no_ext/web_static"

if [ -e "/data/cuisine_static/current" ]; then
    rm -rf /data/web_static/current
fi

ln -s "$path/$no_ext" /data/web_static/current
