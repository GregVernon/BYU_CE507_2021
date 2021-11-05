function vec = import_load(filename)
%IMPORTFILE Import data from a text file
%  vec = import_load(FILENAME) reads data from text file
%  FILENAME for the default selection.  Returns the data as a table.
%  Example:
%  vec = importfile("Beam_Beam_Matrix_LOAD3.mtx", [3, Inf]);
%
%  See also READTABLE.
%

%% Input handling
dataLines = [3, Inf];

%% Set up the Import Options and import the data
opts = delimitedTextImportOptions("NumVariables", 3);

% Specify range and delimiter
opts.DataLines = dataLines;
opts.Delimiter = ",";

% Specify column names and types
opts.VariableNames = ["NodeID", "DOF", "Value"];
opts.VariableTypes = ["double", "double", "double"];

% Specify file level properties
opts.ExtraColumnsRule = "ignore";
opts.EmptyLineRule = "read";

% Import the data
data = readtable(filename, opts);
indices = (data.NodeID - 1) * 3 + data.DOF;
vec(indices,1) = data.Value;

end