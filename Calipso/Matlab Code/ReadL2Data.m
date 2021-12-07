%
%  This example code illustrates how to access and visualize LaRC CALIPSO Lidar
% Level 2 Vertical Feature Mask Version 4 file in MATLAB. 
%
%  If you have any questions, suggestions, comments on this example, 
% please use the HDF-EOS Forum (http://hdfeos.org/forums). 
% 
%  If you would like to see an  example of any other NASA HDF/HDF-EOS
% data product that is not listed in the HDF-EOS  Comprehensive Examples 
% page (http://hdfeos.org/zoo), feel free to contact us at 
% eoshelp@hdfgroup.org or post it at the HDF-EOS Forum 
% (http://hdfeos.org/forums).
%
% Usage:save this script and run (without .m at the end)
%
%  $matlab -nosplash -nodesktop -r CAL_LID_L2_VFM_Standard_V4_10_2012_06_05T20_35_40ZN_hdf
%
% Tested under: MATLAB R2018a
% Last updated: 2019-09-17
clear
import matlab.io.hdf4.*

% Open the HDF4 File.
FILE_NAME = 'CAL_LID_L2_VFM-Standard-V4-21.2021-02-20T10-27-43ZD_Subset.hdf';
SD_id = sd.start(FILE_NAME, 'rdonly');

% Read data.
datafield_name='Feature_Classification_Flags';
sds_index = sd.nameToIndex(SD_id, datafield_name);
sds_id = sd.select(SD_id, sds_index);
data = sd.readData(sds_id);
sd.endAccess(sds_id);

% Read lat.
lat_name='Latitude';
sds_index = sd.nameToIndex(SD_id, lat_name);
sds_id = sd.select(SD_id, sds_index);
lat = sd.readData(sds_id);
sd.endAccess(sds_id);

% Read lon.
lat_name='Longitude';
sds_index = sd.nameToIndex(SD_id, lat_name);
sds_id = sd.select(SD_id, sds_index);
lon = sd.readData(sds_id);
sd.endAccess(sds_id);

% Close the file.
sd.close(SD_id);

% Convert data to double type for plot.
data=double(data);
lat  = double(lat);
lon = double(lon);

% To plot data, you need to fully understand the layout of the 
% Feature_Classification_Flag dataset.
%
% The Feature_Classification_Flag values are stored as a sequence of 5515
%  element arrays (i.e., as an N x 5515 matrix, where N is the number of 
% separate records in the file). In this file, N is 4224.
%
%  Each array represents a 5 km "chunk" of data, 
% and each array element contains the feature classification information for a
%  single range resolution element in the Level 0 lidar data downlinked from 
% the satellite. As shown in the summary below, the vertical and horizontal 
% resolution of the CALIPSO data varies as a function of altitude above mean 
% sea level (see Hunt et al., 2009). 
%
% Here's the summary of number of profiles per 5 km.
% 
% 3 profiles for 20.2km (base) to 30.1km (top) @ 180m
% (index 1-165 / 55 samples per profile)
% 5 profiles for 8.2km (base) to 20.2km (top) @ 60m
% (index 166 - 1165 / 200 samples per profile)
% 15 profiles for -0.5km (base) to 8.2km (top) @ 30m 
% (index 1166 - 5515 / 290 samples per profile)
%
% 3 profiles mean horizontal resolution is 1667m because 3 * 1667m = 5km.
% 55 samples mean vertical resolution is 180m because 55 * 180m = 9.9km  = 
% 30.1km - 20.2km.
%
% In summary, profile size determines horizontal resolution and sample size
% determines the vertical resolution.
%
% Each vertical feature mask record is a 16 bit integer.  See [1] for details.
% Bits | Description
% ----------------
% 1-3  | Feature Type
% 4-5  | Feature Type QA
% ...   |...
% 14-16 | Horizontal averaging
%
% In this example, we'll focus only on "Featrue type."
% 
% However, the resolution of the height will be different.
%
% Altitude Lidar data is in "metadta" [2] stored as HDF4 Vdata. 
% Lidar_Data_Altitudes has 583 records it does not match dataset size
% 565(=55+200+290).
% There are 5 below -0.5km and 30 above 30.1km.
%
% Therefore, we cannot not rely on the Vdata for altitude.
%   
%
% Instead, we should calculate altitude from the data specification.
%
% For each 5515 at a specific lat/lon, we can construct cloud bit vector over 
% altitude.
%
% For example, Feature_Classification_Flags[loc][55] means, 
% Longitude[loc] and altitude = 30.1km.
%
% For another example, Feature_Classification_Flags[loc][56] means, 
% Longitude[loc] + 1667m and altitude = 20.2km.
% 
% There are many possibilites to plot this data.
%
% In this example, we'll focus only on "Cloud" from "Featrue type."
%
% There are many possibilites to plot this data.
%
% Here, we'll subset -05km to 8.2km (e.g., 1166:5515) 
% over latitude approx. 55.8N to 44.6S (e.g., 1:2990)
% and plot altitude vs. latitude.
data = data';
lat = lat';
lon = lon';

% Select the 1-3 bits for Feature Type data. 
% Keep the original for sub-type.
data_ft = bitand(data, 7);

% Use unique() to check range.
% unique(data)
% unique(data_ft)

% Focus on aerosol (=3) data only. Make the rest fill value (= 0).
data(data_ft > 3) = 0;
data(data_ft < 3) = 0;
% unique(data)

% Subset latitude values that are strictly decreasing.
% Otherwise, MATLAB throws the error message "Vector X must be strictly
% increasing or strictly decreasing with no repeated values."
% lat = lat(1:1500);
dim = size(lat, 1);
dim = size(lon, 1);


% You can visualize other blocks by changing subset parameters.
%  data2d = squeeze(data(1:2990, 1:165))    % 20.2km to 30.1km
%  data2d = squeeze(data(1:2990, 166:1165)) %  8.2km to 20.2km
data2d = squeeze(data(:, 1166:5515));   % -0.5km to 8.2km
data3d = reshape(data2d, dim, 290, 15);
data = squeeze(data3d(:,:,1));

% Select the 10-12 bits for Aerosol Type data. 
% 3584 = 0000111000000000
% Keep the original for sub-type.
data_at = bitand(data, 3584);
data_at = bitshift(data_at, -9);

% C = unique(data_at)

% Generate altitude data according to file specification [1].
% You can visualize other blocks by changing subset parameters.
% 20.2km to 30.1km
%for i=0:54
% altitude(i+1) = 20.2 + i*0.18;
%end 

%  8.2km to 20.2km
%for i=0:199
% altitude(i+1) = 8.2 + i*0.06;
%end 

% -0.5km to 8.2km
for i=0:289
 altitude(i+1) = -0.5 + i*0.03;
end 

% Create a Figure to Plot the data.
f = figure('Name', FILE_NAME, ...
    'Renderer', 'zbuffer', ...
    'Position', [0,0,800,600], ...
    'Visible', 'off', ...
    'PaperPositionMode', 'auto');



% Create a custom color map for 8 different Aerosol Type key values.
cmap=[                       %  Key              R   G   B
      [0.00 0.00 0.00];  ... %  0=not determined[000,000,000]    
      [0.00 0.00 1.00];  ... %  1=clean marine  [000,000,255]
      [1.00 1.00 0.00];  ... %  2=dust          [255,255,000]
      [0.00 1.00 0.00];  ... %  3=polluted cont.[000,255,000]
      [1.00 0.00 0.00];  ... %  4=clean cont.   [255,000,000]
      [0.78 0.39 1.00];  ... %  5=polluted dust [200,100,255]
      [0.39 0.20 1.00];  ... %  6=smoke         [100,50,255]
      [0.50 0.50 0.50];  ... %  7=other         [128,128,128]
     ];     

colormap(cmap);
caxis([0 7]); 

contourf(lon, altitude, rot90(data_at, 1));
hold on 
plot([8.4037,8.4037],[-0.5,8.2])


% Set axis labels.
xlabel('Latitude (degrees north)'); 
ylabel('Altitude (km)');


% Put colorbar.
y = [0, 1, 2, 3, 4, 5, 6, 7];
h = colorbar('YTickLabel', {'not determined', 'clear marine', 'dust', ...
                    'polluted continental', 'clear continental', ...
                    'polluted dust', 'smoke', 'other' }, 'YTick', y);

tstring = {FILE_NAME;['Aerosol Type  (Bits 10-12) in' ...
                    ' Feature Classification Flag']};
title(tstring, 'Interpreter', 'none', 'FontSize', 16, ...
      'FontWeight','bold');
saveas(f, [FILE_NAME '.v.m.png']);
% exit;

% References
%
% [1] http://www-calipso.larc.nasa.gov/resources/calipso_users_guide/data_summaries/vfm/index.php
% [2] http://www-calipso.larc.nasa.gov/resources/calipso_users_guide/data_summaries/vfm/index.php#heading03

