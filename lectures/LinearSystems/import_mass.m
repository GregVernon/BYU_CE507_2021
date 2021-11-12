function mtx = import_mass(filename)
%IMPORTFILE Import data from a text file
%  mtx = import_mass(FILENAME) reads data from text file
%  FILENAME for the default selection.  Returns the data as column
%  vectors.
%
%  mtx = import_mass(FILE, DATALINES) reads data for the
%  specified row interval(s) of text file FILENAME. Specify DATALINES as
%  a positive scalar integer or a N-by-2 array of positive scalar
%  integers for dis-contiguous row intervals.
%
%  Example:
%  mtx = import_mass("C:\Users\Owner\Downloads\LinearSystems\Coreform_Report--Level-3-Eigen-Matrix_MASS1.mtx", [1, Inf]);
%
%  See also READTABLE.

%% Input handling
dataLines = [1, Inf];

%% Setup the Import Options and import the data
opts = delimitedTextImportOptions("NumVariables", 3);

% Specify range and delimiter
opts.DataLines = dataLines;
opts.Delimiter = " ";

% Specify column names and types
opts.VariableNames = ["row", "col", "val"];
opts.VariableTypes = ["double", "double", "double"];

% Specify file level properties
opts.ExtraColumnsRule = "ignore";
opts.EmptyLineRule = "read";
opts.ConsecutiveDelimitersRule = "join";
opts.LeadingDelimitersRule = "ignore";

% Import the data
tbl = readtable(filename, opts);

%% Convert to output type
mtx = sparse(tbl.row,tbl.col,tbl.val);
end