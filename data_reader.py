def read_data (path):
    rows = []

    # read the file
    f = open (path, 'r')

    # for the first row, separete them and they are the column names
    colnames = f.readline ().split ()

    # for the rest of the rows, each of them is just one data row
    rows = map (lambda row: dict(zip(colnames, row.split ())), f.readlines ())

    #convert the final column, count, to float and key name to lowercase
    for row in rows:
        row ['count'] = float (row ['Count'])
        del row['Count']

    return rows


if __name__ == '__main__':
    read_data ('data.txt')
