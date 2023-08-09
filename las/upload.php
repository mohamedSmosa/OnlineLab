<?php
$targetDir = "uploads/"; // Directory to store uploaded files

if(isset($_POST["submit"])) {
    $targetFile = $targetDir . basename($_FILES["fileToUpload"]["name"]);
    if (move_uploaded_file($_FILES["fileToUpload"]["tmp_name"], $targetFile)) {
        echo "File uploaded successfully.";
    } else {
        echo "Error uploading file.";
    }
}
?>
