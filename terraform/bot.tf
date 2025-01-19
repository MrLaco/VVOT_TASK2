resource "yandex_function" "bot-function" {
  name               = var.bot_function
  entrypoint         = "index.handler"
  memory             = "128"
  runtime            = "python312"
  user_hash          = data.archive_file.bot-source.output_base64sha256
  service_account_id = yandex_iam_service_account.sa-processing-people-faces-photo.id
  environment = {
    TG_BOT_KEY = var.tg_bot_key
    PHOTOS_BUCKET      = yandex_storage_bucket.photo-bucket.bucket
    FACES_BUCKET       = yandex_storage_bucket.faces-bucket.bucket
    API_GATEWAY_URL    = "https://${yandex_api_gateway.apigw.domain}"
    ACCESS_KEY     = yandex_iam_service_account_static_access_key.sa-processing-people-faces-photo-static-key.access_key
    SECRET_KEY = yandex_iam_service_account_static_access_key.sa-processing-people-faces-photo-static-key.secret_key
  }

  content {
    zip_filename = data.archive_file.bot-source.output_path
  }
}

resource "yandex_function_iam_binding" "bot-function-iam" {
  function_id = yandex_function.bot-function.id
  role        = "functions.functionInvoker"
  members = [
    "system:allUsers",
  ]
}

data "archive_file" "bot-source" {
  type        = "zip"
  source_dir  = "../src/bot"
  output_path = "../build/bot.zip"
}

resource "telegram_bot_webhook" "bot-webhook" {
  url = "https://functions.yandexcloud.net/${yandex_function.bot-function.id}"
}

resource "yandex_api_gateway" "apigw" {
  name = var.apigw
  spec = <<-EOT
openapi: "3.0.0"
info:
  title: Sample API
  version: 1.0.0
paths:
  /:
    get:
      parameters:
        - name: face
          in: query
          required: true
          schema:
            type: string
      x-yc-apigateway-integration:
        type: object_storage
        bucket: ${yandex_storage_bucket.faces-bucket.bucket}
        object: '{face}'
        service_account_id: ${yandex_iam_service_account.sa-processing-people-faces-photo.id}
  /originals/{photo}:
    get:
      parameters:
        - name: photo
          in: path
          required: true
          schema:
            type: string
      x-yc-apigateway-integration:
        type: object_storage
        bucket: ${yandex_storage_bucket.photo-bucket.bucket}
        object: '{photo}'
        service_account_id: ${yandex_iam_service_account.sa-processing-people-faces-photo.id}
EOT
}
