resource "yandex_function" "face-cut-function" {
  name               = var.face_cut_function
  entrypoint         = "index.handler"
  memory             = "128"
  runtime            = "python312"
  user_hash          = data.archive_file.face-cut-source.output_base64sha256
  service_account_id = yandex_iam_service_account.sa-processing-people-faces-photo.id

  environment = {
    ACCESS_KEY     = yandex_iam_service_account_static_access_key.sa-processing-people-faces-photo-static-key.access_key
    SECRET_KEY = yandex_iam_service_account_static_access_key.sa-processing-people-faces-photo-static-key.secret_key
    PHOTOS_BUCKET     = yandex_storage_bucket.photo-bucket.bucket
    FACES_BUCKET      = yandex_storage_bucket.faces-bucket.bucket
  }

  content {
    zip_filename = data.archive_file.face-cut-source.output_path
  }
}

resource "yandex_function_trigger" "task-trigger" {
  name = var.task_trigger

  function {
    id                 = yandex_function.face-cut-function.id
    service_account_id = yandex_iam_service_account.sa-processing-people-faces-photo.id
  }

  message_queue {
    batch_cutoff       = "0"
    batch_size         = "1"
    queue_id           = yandex_message_queue.task-queue.arn
    service_account_id = yandex_iam_service_account.sa-processing-people-faces-photo.id
  }
}

data "archive_file" "face-cut-source" {
  type        = "zip"
  source_dir  = "../src/face-cut"
  output_path = "../build/face-cut.zip"
}
