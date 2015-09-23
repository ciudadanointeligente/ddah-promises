from promises.csv_loader import RowProcessor
import csv, codecs

def csv_unireader(f, encoding="utf-8"):
    for row in csv.reader(codecs.iterencode(codecs.iterdecode(f, encoding), "utf-8")):
        yield [e.decode("utf-8") for e in row]


class CsvProcessor():
    def __init__(self, file_):
        self.file_ = file_

    def work(self):
        rows = []
        for row in csv_unireader(self.file_):
            rows.append(row)
        processor = RowProcessor(rows)
        processor.process()
