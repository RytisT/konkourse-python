konkourse
===============

Documents
===============
code for upload doc button
<form enctype="multipart/form-data" method="post" action="/documents/upload/" class="fileUploadForm">
	<div class="fileupload fileupload-new" data-provides="fileupload" style="text-align:center;" >
		<span class="btn btn-danger btn-file" style="width:190px;"><span class="fileupload-new"><i class="icon-cloud-upload" style="color:#FFF;"></i> Upload Doc</span><span class="fileupload-exists"><i class="icon-cloud-upload" style="color:#FFF;"></i> Upload Doc</span>{{form.file}}</span>
                          <!--
                          this is commented as to hide the file name preview. this widget will upload file on seleciton
                          <span class="fileupload-preview"></span>
                          <a href="#" class="close fileupload-exists" data-dismiss="fileupload" style="float: none">×</a>
                          -->
        </div>
        {% csrf_token %}
		<!--<input class="btn btn-danger btnConvo" type="submit" value="Upload" id="Save"/>-->
</form>