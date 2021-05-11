resource "null_resource" "tagging" {
  
  provisioner "local-exec" {
      command = "git tag -a $(docker run --rm -v $(pwd):/repo codacy/git-version) -m '$(git log -1 --pretty=%B)'"
  }
 
}

resource "null_resource" "publish" {
  
  provisioner "local-exec" {
      command = "git push --tags"
  }
  depends_on = [
    null_resource.tagging
  ]
 
}