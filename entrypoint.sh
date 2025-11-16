#!/bin/sh

# Make sure uploads directory exists
mkdir -p /uploads

# Copy initial files to /uploads if the volume is empty
if [ -z "$(ls -A /uploads)" ]; then
    echo "Copying initial files to /uploads..."
    cp -r /app/uploads_init/* /uploads/
else
    echo "Uploads volume already has files. Skipping copy."
fi

# Run the main CMD
exec "$@"
