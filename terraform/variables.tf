variable "cloud_id" {
  type = string
}

variable "folder_id" {
  type = string
}

variable "sa_key_file_path" {
  type    = string
  default = "~/.yc-keys/key.json"
}

variable "tg_bot_key" {
  type = string
}

variable "sa_processing_people_faces_photo" {
  type    = string
  default = "sa-processing-people-faces-photo"
}

variable "photo_bucket" {
  type    = string
  default = "vvot38-photo"
}

variable "face_detection_function" {
  type    = string
  default = "vvot38-face-detection"
}

variable "photo_trigger" {
  type    = string
  default = "vvot38-photo"
}

variable "task_queue" {
  type    = string
  default = "vvot38-task"
}

variable "faces_bucket" {
  type    = string
  default = "vvot38-faces"
}

variable "face_cut_function" {
  type    = string
  default = "vvot38-face-cut"
}

variable "task_trigger" {
  type    = string
  default = "vvot38-task"
}

variable "bot_function" {
  type    = string
  default = "vvot38-boot"
}

variable "apigw" {
  type    = string
  default = "vvot38-apigw"
}
