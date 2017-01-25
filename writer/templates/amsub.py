import numpy as np
from xarray import Variable

from writer.default_data import DefaultData
from writer.templates.templateutil import TemplateUtil

NUM_CHANNELS = 5
BTEMPS_FILL_VALUE = -999999
SWATH_WIDTH = 90


class AMSUB:
    @staticmethod
    def add_original_variables(dataset, height):
        TemplateUtil.add_geolocation_variables(dataset, SWATH_WIDTH, height)

        # btemps
        default_array = DefaultData.create_default_array_3d(SWATH_WIDTH, height, NUM_CHANNELS, np.int32,
                                                            BTEMPS_FILL_VALUE)
        variable = Variable(["channel", "y", "x"], default_array)
        variable.attrs["_FillValue"] = BTEMPS_FILL_VALUE
        variable.attrs["standard_name"] = "toa_brightness_temperature"
        variable.attrs["units"] = "K"
        variable.attrs["scale_factor"] = 0.01
        variable.attrs["ancillary_variables"] = "chanqual qualind scanqual"
        dataset["btemps"] = variable

        # chanqual
        default_array = DefaultData.create_default_array(height, NUM_CHANNELS, np.int32, dims_names=["channel", "y"],
                                                         fill_value=0)
        variable = Variable(["channel", "y"], default_array)
        variable.attrs["standard_name"] = "status_flag"
        dataset["chanqual"] = variable

        # instrtemp
        default_array = DefaultData.create_default_vector(height, np.int32)
        variable = Variable(["y"], default_array)
        variable.attrs["_FillValue"] = DefaultData.get_default_fill_value(np.int32)
        variable.attrs["units"] = "K"
        variable.attrs["scale_factor"] = 0.01
        dataset["instrtemp"] = variable

        # qualind
        default_array = DefaultData.create_default_vector(height, np.int32, fill_value=0)
        variable = Variable(["y"], default_array)
        variable.attrs["standard_name"] = "status_flag"
        dataset["qualind"] = variable

        # scanqual
        default_array = DefaultData.create_default_vector(height, np.int32, fill_value=0)
        variable = Variable(["y"], default_array)
        variable.attrs["standard_name"] = "status_flag"
        dataset["scanqual"] = variable

        # scnlin
        default_array = DefaultData.create_default_vector(height, np.int32)
        variable = Variable(["y"], default_array)
        variable.attrs["_FillValue"] = DefaultData.get_default_fill_value(np.int32)
        variable.attrs["standard_name"] = "scanline"
        dataset["scnlin"] = variable

        # scnlindy
        default_array = DefaultData.create_default_vector(height, np.int32)
        variable = Variable(["y"], default_array)
        variable.attrs["_FillValue"] = DefaultData.get_default_fill_value(np.int32)
        variable.attrs["standard_name"] = "scanline day"
        dataset["scnlindy"] = variable

        # scnlintime
        default_array = DefaultData.create_default_vector(height, np.int32)
        variable = Variable(["y"], default_array)
        variable.attrs["_FillValue"] = DefaultData.get_default_fill_value(np.int32)
        variable.attrs["standard_name"] = "scanline time"
        variable.attrs["long_name"] = "Acquisition time of scan in milliseconds since beginning of the day"
        variable.attrs["units"] = "ms"
        dataset["scnlintime"] = variable

        # scnlinyr
        default_array = DefaultData.create_default_vector(height, np.int32)
        variable = Variable(["y"], default_array)
        variable.attrs["_FillValue"] = DefaultData.get_default_fill_value(np.int32)
        variable.attrs["standard_name"] = "scanline year"
        dataset["scnlinyr"] = variable

        # satellite_azimuth_angle
        variable = AMSUB.create_angle_variable(height, "sensor_azimuth_angle")
        dataset["satellite_azimuth_angle"] = variable

        # satellite_zenith_angle
        variable = AMSUB.create_angle_variable(height, "sensor_zenith_angle")
        dataset["satellite_zenith_angle"] = variable

        # solar_azimuth_angle
        variable = AMSUB.create_angle_variable(height, "solar_azimuth_angle")
        dataset["solar_azimuth_angle"] = variable

        # solar_zenith_angle
        variable = AMSUB.create_angle_variable(height, "solar_zenith_angle")
        dataset["solar_zenith_angle"] = variable

    @staticmethod
    def get_swath_width():
        return SWATH_WIDTH

    @staticmethod
    def add_uncertainty_variables(dataset, height):
        # u_btemps
        default_array = DefaultData.create_default_array_3d(SWATH_WIDTH, height, NUM_CHANNELS, np.float32)
        variable = Variable(["channel", "y", "x"], default_array)
        variable.attrs["_FillValue"] = DefaultData.get_default_fill_value(np.float32)
        variable.attrs["standard_name"] = "total uncertainty of brightness temperature"
        variable.attrs["units"] = "K"
        dataset["u_btemps"] = variable

        # u_syst_btemps
        default_array = DefaultData.create_default_array_3d(SWATH_WIDTH, height, NUM_CHANNELS, np.float32)
        variable = Variable(["channel", "y", "x"], default_array)
        variable.attrs["_FillValue"] = DefaultData.get_default_fill_value(np.float32)
        variable.attrs["standard_name"] = "systematic uncertainty of brightness temperature"
        variable.attrs["units"] = "K"
        dataset["u_syst_btemps"] = variable

        # u_random_btemps
        default_array = DefaultData.create_default_array_3d(SWATH_WIDTH, height, NUM_CHANNELS, np.float32)
        variable = Variable(["channel", "y", "x"], default_array)
        variable.attrs["_FillValue"] = DefaultData.get_default_fill_value(np.float32)
        variable.attrs["standard_name"] = "noise on brightness temperature"
        variable.attrs["units"] = "K"
        dataset["u_random_btemps"] = variable

        # u_instrtemp
        default_array = DefaultData.create_default_vector(height, np.float32)
        variable = Variable(["y"], default_array)
        variable.attrs["_FillValue"] = DefaultData.get_default_fill_value(np.float32)
        variable.attrs["standard_name"] = "uncertainty of instrument temperature"
        variable.attrs["units"] = "K"
        dataset["u_instrtemp"] = variable

        # u_latitude
        variable = AMSUB.create_angle_uncertainty_variable("latitude", height)
        dataset["u_latitude"] = variable

        # u_longitude
        variable = AMSUB.create_angle_uncertainty_variable("longitude", height)
        dataset["u_longitude"] = variable

        # u_satellite_azimuth_angle
        variable = AMSUB.create_angle_uncertainty_variable("satellite azimuth angle", height)
        dataset["u_satellite_azimuth_angle"] = variable

        # u_satellite_zenith_angle
        variable = AMSUB.create_angle_uncertainty_variable("satellite zenith angle", height)
        dataset["u_satellite_zenith_angle"] = variable

        # u_solar_azimuth_angle
        variable = AMSUB.create_angle_uncertainty_variable("solar azimuth angle", height)
        dataset["u_solar_azimuth_angle"] = variable

        # u_solar_zenith_angle
        variable = AMSUB.create_angle_uncertainty_variable("solar zenith angle", height)
        dataset["u_solar_zenith_angle"] = variable

    @staticmethod
    def create_angle_uncertainty_variable(angle_name, height):
        default_array = DefaultData.create_default_array(SWATH_WIDTH, height, np.float32)
        variable = Variable(["y", "x"], default_array)
        variable.attrs["_FillValue"] = DefaultData.get_default_fill_value(np.float32)
        variable.attrs["standard_name"] = "uncertainty of " + angle_name
        variable.attrs["units"] = "degree"
        return variable

    @staticmethod
    def create_angle_variable(height, standard_name):
        default_array = DefaultData.create_default_array(SWATH_WIDTH, height, np.int32, fill_value=-999999)
        variable = Variable(["y", "x"], default_array)
        variable.attrs["_FillValue"] = -999999
        variable.attrs["standard_name"] = standard_name
        variable.attrs["units"] = "degree"
        variable.attrs["scale_factor"] = 0.01
        return variable
