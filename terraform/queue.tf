resource "yandex_message_queue" "task-queue" {
  name       = var.task_queue
  access_key = yandex_iam_service_account_static_access_key.sa-processing-people-faces-photo-static-key.access_key
  secret_key = yandex_iam_service_account_static_access_key.sa-processing-people-faces-photo-static-key.secret_key
}
