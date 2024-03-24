#!/usr/bin/bash
# Compiles and sets up server to serve static content

`cp -u web_flask/static/images/* web_static/images`
if [ -e "versions" ]
then
   echo ""
else
   `mkdir versions`
fi

# Get current timestamp
timestamp=$(date +"%Y%m%d%H%M%S")

# Create the tar file
tar -czvf "versions/web_static_$timestamp.tgz" ./web_static/


# Extract the filename
file_n=$(basename $1)

# Print the filename
echo "$file_n"



# Remove the extension
no_ext="${file_n%.*}"

# Print the filename without extension
echo "$no_ext"

path="/data/cuisine_static/releases/"

`cp $1 /tmp`
`mkdir -p $path$no_ext`
`tar -xzf /tmp/$file_n -C $path/$no_ext`
`mv $path/$no_ext/web_static/* $path/$no_ext`
`rm -rf $path/$no_ext/web_static`

if [ -e "/data/cuisine_static/current" ]
then
    `rm -rf /data/web_static/current`
fi

`ln -s $path/$no_ext /data/web_static/current
