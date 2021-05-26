zip_file_name=icorr-alexa-skill.zip
function_name="icorr-alexa-skill"

# mkdir bundle
# pip install -r requirements.txt -t ./bundle/
# rm ${zip_file_name}
# zip -r ${zip_file_name} . -x "*.git*" -x "deploy.sh" -x "*.png" -x "*.html"

aws lambda update-function-code --function-name ${function_name} --zip-file fileb://./${zip_file_name}
