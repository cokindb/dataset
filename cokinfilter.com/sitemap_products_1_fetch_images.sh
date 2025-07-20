#!/bin/bash
#
# Downloads image_urls
#


base_dir="${PWD}"
output_dir="${base_dir}/images"

image_urls=$( jq -r .[].image_url cokin_products_concise.json )

while read image_url; do
	image_id=$( echo -n "${image_url}" | md5sum | cut -d " " -f 1 )
	output_filename="${output_dir}/${image_id}.jpg"

	curl -s -o "${output_filename}" "${image_url}"
	RC="$?"

	echo "${RC} ${image_id} ${output_filename} ${image_url}"

done <<< "${image_urls}"
