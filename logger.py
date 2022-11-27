
import csv


class Logger:
    def __init__(self, column_names: list[str]):
        self.data: dict[str, list[float]] = {}
        #Initialize all columns to []
        for name in column_names: self.data[name] = []

    def add_data(self, name: str, value: float):
        """Append data to a given column name. Raises KeyError if the column does not exist."""
        if name in self.data:
            self.data[name].append(value)
        else:
            raise KeyError("Key {} not found".format(name))

    def write(self):
        """Write the output data to 'output.csv'."""
        with open("output.csv", 'w') as csvout:
            writer = csv.writer(csvout)
            
            row = []
            #Write the column names
            for name in self.data: row.append(name)
            writer.writerow(row)
            
            # The csv writer object writes in rows, whereas our data is organized in columns. 
            # To write our data, we need to loop through every column, collecting the entries 
            # in a row. We then write that row and continue to the next. This loops until 
            # all data has been written. In the case of one column being longer than the rest, 
            # an empty string is written to the remaining empty cells.
            should_continue: bool = True 
            curr_idx: int = 0

            while should_continue:
                should_continue = False 
                row = []
                
                #Loop through columns
                for name in self.data:

                    #If there are still entries in the column, write them
                    if curr_idx < len(self.data[name]):
                        should_continue = True 
                        row.append(self.data[name][curr_idx])
                    #Otherwise, write an empty string
                    else: row.append("")

                writer.writerow(row)
                
                curr_idx += 1

