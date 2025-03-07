import savReaderWriter
from collections.abc import Iterable

with savReaderWriter.SavReader("data.sav") as reader:
    records = reader.all()
    df = pd.DataFrame(records, columns=[var for var in reader.header])
print(df.head())
