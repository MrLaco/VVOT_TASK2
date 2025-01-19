resource "yandex_function" "face-detection-function" {
  name               = var.face_detection_function
  entrypoint         = "index.handler"
  memory             = "512"
  runtime            = "python312"
  user_hash          = data.archive_file.face-detection-source.output_base64sha256
  service_account_id = yandex_iam_service_account.sa-processing-people-faces-photo.id

  environment = {
    ACCESS_KEY     = yandex_iam_service_account_static_access_key.sa-processing-people-faces-photo-static-key.access_key
    SECRET_KEY = yandex_iam_service_account_static_access_key.sa-processing-people-faces-photo-static-key.secret_key
    BUCKET            = yandex_storage_bucket.photo-bucket.bucket
    QUEUE_URL         = yandex_message_queue.task-queue.id
  }

  content {
    zip_filename = data.archive_file.face-detection-source.output_path
  }
}

resource "yandex_function_trigger" "photo-trigger" {
  name = var.photo_trigger

  function {
    id                 = yandex_function.face-detection-function.id
    service_account_id = yandex_iam_service_account.sa-processing-people-faces-photo.id
  }

  object_storage {
    bucket_id    = yandex_storage_bucket.photo-bucket.id
    suffix       = ".jpg"
    create       = true
    batch_cutoff = "0"
    batch_size   = "1"
  }
}

data "archive_file" "face-detection-source" {
  type        = "zip"
  source_dir  = "../src/face-detection"
  output_path = "../build/face-detection.zip"
}
