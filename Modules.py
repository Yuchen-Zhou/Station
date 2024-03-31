class UserInfo:
    def __init__(self, username, email, storage, used, used_signal, percentage):
        self.UserName = username
        self.UserEmail = email
        self.UserStorage = storage
        self.UserUsed = used
        self.UserUsedSignal = used_signal
        self.UserPercentage = percentage

    def tojson(self):
        return {
            'username': self.UserName,
            'email': self.UserEmail,
            'storage': self.UserStorage,
            'used': self.UserUsed,
            'used_signal': self.UserUsedSignal,
            'percentage': self.UserPercentage
        }


class File:

    # File参数文件名、文件类型、文件大小、上传时间、上传文件夹
    def __init__(self, name, file_type, size, signal, upload_time, folder_name=None):
        self.name = name
        self.file_type = file_type
        self.size = size
        self.signal = signal
        self.upload_time = upload_time
        self.folder_name = folder_name


class Folder:
    def __init__(self, name, file_type, size, signal, upload_time):
        self.name = name
        self.file_type = file_type
        self.size = size
        self.signal = signal
        self.upload_time = upload_time
