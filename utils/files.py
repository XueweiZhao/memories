import os


class MemoryFile:
    def __init__(self, year, month, day):
        self._year = year
        self._month = month
        self._day = day

        self.file = 'memories/{}-{}-{}.md'.format(year, month, day)
        self.preview_file = 'memories/{}-preview.md'.format(year, month, day)

    def _exists(self, file):
        return os.path.isfile(file)

    def _create(self, file):
        dir_name = os.path.dirname(file) or '.'
        try:
            os.makedirs(dir_name)
        except OSError:  # Already exists
            pass

    def _delete(self, file):
        os.remove(file)

    def _get(self, file):
        try:
            with open(file) as f:
                content = f.read()
        except FileNotFoundError:
            content = ''
        return content

    def _write(self, content, file):
        self._create(file)
        out_file = open(file, 'w+')
        out_file.write(content)
        out_file.close()

    def exists(self):
        return self._exists(self.file)

    def get_content(self):
        return self._get(self.file)

    def get_preview_content(self):
        content = self._get(self.preview_file)
        if not content:
            content = self._get(self.file)
            self._write(content, self.preview_file)
        return content

    def write_preview(self, content):
        self._write(content, self.preview_file)

    def save_preview(self):
        content = self._get(self.preview_file)
        self._write(content, self.file)
        self._delete(self.preview_file)
