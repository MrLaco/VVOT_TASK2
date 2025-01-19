resource "yandex_storage_bucket" "photo-bucket" {
  bucket = var.photo_bucket
}

resource "yandex_storage_bucket" "faces-bucket" {
  bucket = var.faces_bucket
}
