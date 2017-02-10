import unittest

import numpy as np
import xarray as xr

from writer.default_data import DefaultData
from writer.templates.avhrr import AVHRR


class AVHRRTest(unittest.TestCase):
    def test_add_original_variables(self):
        ds = xr.Dataset()
        AVHRR.add_original_variables(ds, 5)

        latitude = ds.variables["latitude"]
        self.assertEqual((5, 409), latitude.shape)
        self.assertEqual(-32768.0, latitude.data[0, 0])
        self.assertEqual(-32768.0, latitude.attrs["_FillValue"])
        self.assertEqual("latitude", latitude.attrs["standard_name"])
        self.assertEqual("degrees_north", latitude.attrs["units"])

        longitude = ds.variables["longitude"]
        self.assertEqual((5, 409), longitude.shape)
        self.assertEqual(-32768.0, longitude.data[0, 1])
        self.assertEqual(-32768.0, longitude.attrs["_FillValue"])
        self.assertEqual("longitude", longitude.attrs["standard_name"])
        self.assertEqual("degrees_east", longitude.attrs["units"])

        time = ds.variables["Time"]
        self.assertEqual((5, 409), time.shape)
        self.assertEqual(DefaultData.get_default_fill_value(np.float32), time.data[0, 2])
        self.assertEqual(DefaultData.get_default_fill_value(np.float32), time.attrs["_FillValue"])
        self.assertEqual("time", time.attrs["standard_name"])
        self.assertEqual("Acquisition time in seconds since 1970-01-01 00:00:00", time.attrs["long_name"])
        self.assertEqual("s", time.attrs["units"])

        scanline = ds.variables["scanline"]
        self.assertEqual((5,), scanline.shape)
        self.assertEqual(DefaultData.get_default_fill_value(np.int16), scanline.data[3])
        self.assertEqual(DefaultData.get_default_fill_value(np.int16), scanline.attrs["_FillValue"])
        self.assertEqual("scanline", scanline.attrs["standard_name"])
        self.assertEqual("Level 1b line number", scanline.attrs["long_name"])
        self.assertEqual(0, scanline.attrs["valid_min"])

        sat_azimuth = ds.variables["satellite_azimuth_angle"]
        self.assertEqual((5, 409), sat_azimuth.shape)
        self.assertEqual(DefaultData.get_default_fill_value(np.float32), sat_azimuth.data[0, 4])
        self.assertEqual(DefaultData.get_default_fill_value(np.float32), sat_azimuth.attrs["_FillValue"])
        self.assertEqual("sensor_azimuth_angle", sat_azimuth.attrs["standard_name"])
        self.assertEqual("degree", sat_azimuth.attrs["units"])

        sat_zenith = ds.variables["satellite_zenith_angle"]
        self.assertEqual((5, 409), sat_zenith.shape)
        self.assertEqual(DefaultData.get_default_fill_value(np.int16), sat_zenith.data[0, 5])
        self.assertEqual(DefaultData.get_default_fill_value(np.int16), sat_zenith.attrs["_FillValue"])
        self.assertEqual("sensor_zenith_angle", sat_zenith.attrs["standard_name"])
        self.assertEqual(0.0, sat_zenith.attrs["add_offset"])
        self.assertEqual(0.01, sat_zenith.attrs["scale_factor"])
        self.assertEqual("degree", sat_zenith.attrs["units"])
        self.assertEqual(9000, sat_zenith.attrs["valid_max"])
        self.assertEqual(0, sat_zenith.attrs["valid_min"])

        sol_azimuth = ds.variables["solar_azimuth_angle"]
        self.assertEqual(DefaultData.get_default_fill_value(np.float32), sol_azimuth.data[0, 6])
        self.assertEqual(DefaultData.get_default_fill_value(np.float32), sol_azimuth.attrs["_FillValue"])
        self.assertEqual("solar_azimuth_angle", sol_azimuth.attrs["standard_name"])
        self.assertEqual("degree", sol_azimuth.attrs["units"])

        sol_zenith = ds.variables["solar_zenith_angle"]
        self.assertEqual((5, 409), sol_zenith.shape)
        self.assertEqual(DefaultData.get_default_fill_value(np.int16), sol_zenith.data[0, 7])
        self.assertEqual(DefaultData.get_default_fill_value(np.int16), sol_zenith.attrs["_FillValue"])
        self.assertEqual("solar_zenith_angle", sol_zenith.attrs["standard_name"])
        self.assertEqual(0.0, sol_zenith.attrs["add_offset"])
        self.assertEqual(0.01, sol_zenith.attrs["scale_factor"])
        self.assertEqual("degree", sol_zenith.attrs["units"])
        self.assertEqual(18000, sol_zenith.attrs["valid_max"])
        self.assertEqual(0, sol_zenith.attrs["valid_min"])

        ch1_bt = ds.variables["Ch1_Bt"]
        self._assert_correct_refl_variable(ch1_bt, "Channel 1 Reflectance")

        ch2_bt = ds.variables["Ch2_Bt"]
        self._assert_correct_refl_variable(ch2_bt, "Channel 2 Reflectance")

        ch3a_bt = ds.variables["Ch3a_Bt"]
        self._assert_correct_refl_variable(ch3a_bt, "Channel 3a Reflectance")

        ch3b_bt = ds.variables["Ch3b_Bt"]
        self._assert_correct_bt_variable(ch3b_bt, "Channel 3b Brightness Temperature")

        ch4_bt = ds.variables["Ch4_Bt"]
        self._assert_correct_bt_variable(ch4_bt, "Channel 4 Brightness Temperature")

        ch5_bt = ds.variables["Ch5_Bt"]
        self._assert_correct_bt_variable(ch5_bt, "Channel 5 Brightness Temperature")

        ict_temp = ds.variables["T_ICT"]
        self.assertEqual((5,), ict_temp.shape)
        self.assertEqual(DefaultData.get_default_fill_value(np.int16), ict_temp.data[1])
        self.assertEqual(DefaultData.get_default_fill_value(np.int16), ict_temp.attrs["_FillValue"])
        self.assertEqual("Temperature of the internal calibration target", ict_temp.attrs["standard_name"])
        self.assertEqual(273.15, ict_temp.attrs["add_offset"])
        self.assertEqual(0.01, ict_temp.attrs["scale_factor"])
        self.assertEqual("K", ict_temp.attrs["units"])
        self.assertEqual(10000, ict_temp.attrs["valid_max"])
        self.assertEqual(-20000, ict_temp.attrs["valid_min"])

    def test_get_swath_width(self):
        self.assertEqual(409, AVHRR.get_swath_width())

    def test_add_uncertainty_variables(self):
        ds = xr.Dataset()
        AVHRR.add_uncertainty_variables(ds, 5)

        u_latitude = ds.variables["u_latitude"]
        self.assertEqual((5, 409), u_latitude.shape)
        self.assertEqual(DefaultData.get_default_fill_value(np.float32), u_latitude.data[0, 34])
        self.assertEqual(DefaultData.get_default_fill_value(np.float32), u_latitude.attrs["_FillValue"])
        self.assertEqual("uncertainty of latitude", u_latitude.attrs["standard_name"])
        self.assertEqual("degree", u_latitude.attrs["units"])

        u_longitude = ds.variables["u_longitude"]
        self.assertEqual((5, 409), u_longitude.shape)
        self.assertEqual(DefaultData.get_default_fill_value(np.float32), u_longitude.data[0, 34])
        self.assertEqual(DefaultData.get_default_fill_value(np.float32), u_longitude.attrs["_FillValue"])
        self.assertEqual("uncertainty of longitude", u_longitude.attrs["standard_name"])
        self.assertEqual("degree", u_longitude.attrs["units"])

        u_time = ds.variables["u_time"]
        self.assertEqual((5, 409), u_time.shape)
        self.assertEqual(DefaultData.get_default_fill_value(np.float32), u_time.data[1, 35])
        self.assertEqual(DefaultData.get_default_fill_value(np.float32), u_time.attrs["_FillValue"])
        self.assertEqual("uncertainty of time", u_time.attrs["standard_name"])
        self.assertEqual("s", u_time.attrs["units"])

        u_sat_azimuth = ds.variables["u_satellite_azimuth_angle"]
        self.assertEqual((5, 409), u_sat_azimuth.shape)
        self.assertEqual(DefaultData.get_default_fill_value(np.float32), u_sat_azimuth.data[2, 36])
        self.assertEqual(DefaultData.get_default_fill_value(np.float32), u_sat_azimuth.attrs["_FillValue"])
        self.assertEqual("uncertainty of satellite azimuth angle", u_sat_azimuth.attrs["standard_name"])
        self.assertEqual("degree", u_sat_azimuth.attrs["units"])

        u_sat_zenith = ds.variables["u_satellite_zenith_angle"]
        self.assertEqual((5, 409), u_sat_zenith.shape)
        self.assertEqual(DefaultData.get_default_fill_value(np.float32), u_sat_zenith.data[2, 36])
        self.assertEqual(DefaultData.get_default_fill_value(np.float32), u_sat_zenith.attrs["_FillValue"])
        self.assertEqual("uncertainty of satellite zenith angle", u_sat_zenith.attrs["standard_name"])
        self.assertEqual("degree", u_sat_zenith.attrs["units"])

        u_sol_azimuth = ds.variables["u_solar_azimuth_angle"]
        self.assertEqual((5, 409), u_sol_azimuth.shape)
        self.assertEqual(DefaultData.get_default_fill_value(np.float32), u_sol_azimuth.data[2, 36])
        self.assertEqual(DefaultData.get_default_fill_value(np.float32), u_sol_azimuth.attrs["_FillValue"])
        self.assertEqual("uncertainty of solar azimuth angle", u_sol_azimuth.attrs["standard_name"])
        self.assertEqual("degree", u_sol_azimuth.attrs["units"])

        u_sol_zenith = ds.variables["u_solar_zenith_angle"]
        self.assertEqual((5, 409), u_sol_zenith.shape)
        self.assertEqual(DefaultData.get_default_fill_value(np.float32), u_sol_zenith.data[2, 36])
        self.assertEqual(DefaultData.get_default_fill_value(np.float32), u_sol_zenith.attrs["_FillValue"])
        self.assertEqual("uncertainty of solar zenith angle", u_sol_zenith.attrs["standard_name"])
        self.assertEqual("degree", u_sol_zenith.attrs["units"])

        prt_c = ds.variables["PRT_C"]
        self.assertEqual((5, 3), prt_c.shape)
        self.assertEqual(DefaultData.get_default_fill_value(np.int16), prt_c.data[3, 2])
        self.assertEqual(DefaultData.get_default_fill_value(np.int16), prt_c.attrs["_FillValue"])
        self.assertEqual("Prt counts", prt_c.attrs["standard_name"])
        self.assertEqual("count", prt_c.attrs["units"])

        u_prt = ds.variables["u_prt"]
        self.assertEqual((5, 3), u_prt.shape)
        self.assertEqual(DefaultData.get_default_fill_value(np.float32), u_prt.data[4, 0])
        self.assertEqual(DefaultData.get_default_fill_value(np.float32), u_prt.attrs["_FillValue"])
        self.assertEqual("Uncertainty on the PRT counts", u_prt.attrs["standard_name"])
        self.assertEqual("count", u_prt.attrs["units"])

        r_ict = ds.variables["R_ICT"]
        self.assertEqual((5, 3), r_ict.shape)
        self.assertEqual(DefaultData.get_default_fill_value(np.float32), r_ict.data[0, 1])
        self.assertEqual(DefaultData.get_default_fill_value(np.float32), r_ict.attrs["_FillValue"])
        self.assertEqual("Radiance of the PRT", r_ict.attrs["standard_name"])
        self.assertEqual("mW m^-2 sr^-1 cm", r_ict.attrs["units"])

        t_instr = ds.variables["T_instr"]
        self.assertEqual((5,), t_instr.shape)
        self.assertEqual(DefaultData.get_default_fill_value(np.float32), t_instr.data[2])
        self.assertEqual(DefaultData.get_default_fill_value(np.float32), t_instr.attrs["_FillValue"])
        self.assertEqual("Instrument temperature", t_instr.attrs["standard_name"])
        self.assertEqual("K", t_instr.attrs["units"])

        self._assert_correct_counts_variable(ds, "Ch1_Csp", "Ch1 Space counts")
        self._assert_correct_counts_variable(ds, "Ch2_Csp", "Ch2 Space counts")
        self._assert_correct_counts_variable(ds, "Ch3a_Csp", "Ch3a Space counts")
        self._assert_correct_counts_variable(ds, "Ch3b_Csp", "Ch3b Space counts")
        self._assert_correct_counts_variable(ds, "Ch4_Csp", "Ch4 Space counts")
        self._assert_correct_counts_variable(ds, "Ch5_Csp", "Ch5 Space counts")

        self._assert_correct_counts_variable(ds, "Ch3b_Cict", "Ch3b ICT counts")
        self._assert_correct_counts_variable(ds, "Ch4_Cict", "Ch4 ICT counts")
        self._assert_correct_counts_variable(ds, "Ch5_Cict", "Ch5 ICT counts")

        self._assert_correct_counts_variable(ds, "Ch1_Ce", "Ch1 Earth counts")
        self._assert_correct_counts_variable(ds, "Ch2_Ce", "Ch2 Earth counts")
        self._assert_correct_counts_variable(ds, "Ch3a_Ce", "Ch3a Earth counts")
        self._assert_correct_counts_variable(ds, "Ch3b_Ce", "Ch3b Earth counts")
        self._assert_correct_counts_variable(ds, "Ch4_Ce", "Ch4 Earth counts")
        self._assert_correct_counts_variable(ds, "Ch5_Ce", "Ch5 Earth counts")

        self._assert_correct_counts_uncertainty_variable(ds, "Ch1_u_Csp", "Ch1 Uncertainty on space counts")
        self._assert_correct_counts_uncertainty_variable(ds, "Ch2_u_Csp", "Ch2 Uncertainty on space counts")
        self._assert_correct_counts_uncertainty_variable(ds, "Ch3a_u_Csp", "Ch3a Uncertainty on space counts")
        self._assert_correct_counts_uncertainty_variable(ds, "Ch3b_u_Csp", "Ch3b Uncertainty on space counts")
        self._assert_correct_counts_uncertainty_variable(ds, "Ch4_u_Csp", "Ch4 Uncertainty on space counts")
        self._assert_correct_counts_uncertainty_variable(ds, "Ch5_u_Csp", "Ch5 Uncertainty on space counts")

        self._assert_correct_counts_uncertainty_variable(ds, "Ch3b_u_Cict", "Ch3b Uncertainty on ICT counts")
        self._assert_correct_counts_uncertainty_variable(ds, "Ch4_u_Cict", "Ch4 Uncertainty on ICT counts")
        self._assert_correct_counts_uncertainty_variable(ds, "Ch5_u_Cict", "Ch5 Uncertainty on ICT counts")

        self._assert_correct_counts_uncertainty_variable(ds, "Ch1_u_Ce", "Ch1 Uncertainty on earth counts")
        self._assert_correct_counts_uncertainty_variable(ds, "Ch2_u_Ce", "Ch2 Uncertainty on earth counts")
        self._assert_correct_counts_uncertainty_variable(ds, "Ch3a_u_Ce", "Ch3a Uncertainty on earth counts")
        self._assert_correct_counts_uncertainty_variable(ds, "Ch3b_u_Ce", "Ch3b Uncertainty on earth counts")
        self._assert_correct_counts_uncertainty_variable(ds, "Ch4_u_Ce", "Ch4 Uncertainty on earth counts")
        self._assert_correct_counts_uncertainty_variable(ds, "Ch5_u_Ce", "Ch5 Uncertainty on earth counts")

        self._assert_correct_refl_uncertainty_variable(ds, "Ch1_u_Refl", "Ch1 Total uncertainty on reflectance")
        self._assert_correct_refl_uncertainty_variable(ds, "Ch2_u_Refl", "Ch2 Total uncertainty on reflectance")
        self._assert_correct_refl_uncertainty_variable(ds, "Ch3a_u_Refl", "Ch3a Total uncertainty on reflectance")

        self._assert_correct_bt_uncertainty_variable(ds, "Ch3b_u_Bt", "Ch3b Total uncertainty on brightness temperature")
        self._assert_correct_bt_uncertainty_variable(ds, "Ch4_u_Bt", "Ch4 Total uncertainty on brightness temperature")
        self._assert_correct_bt_uncertainty_variable(ds, "Ch5_u_Bt", "Ch5 Total uncertainty on brightness temperature")

        self._assert_correct_bt_uncertainty_variable(ds, "Ch3b_ur_Bt", "Ch3b Random uncertainty on brightness temperature")
        self._assert_correct_bt_uncertainty_variable(ds, "Ch4_ur_Bt", "Ch4 Random uncertainty on brightness temperature")
        self._assert_correct_bt_uncertainty_variable(ds, "Ch5_ur_Bt", "Ch5 Random uncertainty on brightness temperature")

        self._assert_correct_bt_uncertainty_variable(ds, "Ch3b_us_Bt", "Ch3b Systematic uncertainty on brightness temperature")
        self._assert_correct_bt_uncertainty_variable(ds, "Ch4_us_Bt", "Ch4 Systematic uncertainty on brightness temperature")
        self._assert_correct_bt_uncertainty_variable(ds, "Ch5_us_Bt", "Ch5 Systematic uncertainty on brightness temperature")

    def _assert_correct_counts_variable(self, ds, name, standard_name):
        variable = ds.variables[name]
        self.assertEqual((5, 409), variable.shape)
        self.assertEqual(DefaultData.get_default_fill_value(np.int32), variable.data[3, 306])
        self.assertEqual(DefaultData.get_default_fill_value(np.int32), variable.attrs["_FillValue"])
        self.assertEqual(standard_name, variable.attrs["standard_name"])
        self.assertEqual("count", variable.attrs["units"])

    def _assert_correct_counts_uncertainty_variable(self, ds, name, standard_name):
        variable = ds.variables[name]
        self.assertEqual((5, 409), variable.shape)
        self.assertEqual(DefaultData.get_default_fill_value(np.float32), variable.data[4, 307])
        self.assertEqual(DefaultData.get_default_fill_value(np.float32), variable.attrs["_FillValue"])
        self.assertEqual(standard_name, variable.attrs["standard_name"])
        self.assertEqual("count", variable.attrs["units"])

    def _assert_correct_refl_uncertainty_variable(self, ds, name, standard_name):
        variable = ds.variables[name]
        self.assertEqual((5, 409), variable.shape)
        self.assertEqual(DefaultData.get_default_fill_value(np.float32), variable.data[4, 307])
        self.assertEqual(DefaultData.get_default_fill_value(np.float32), variable.attrs["_FillValue"])
        self.assertEqual(standard_name, variable.attrs["standard_name"])
        self.assertEqual("percent", variable.attrs["units"])

    def _assert_correct_bt_uncertainty_variable(self, ds, name, standard_name):
        variable = ds.variables[name]
        self.assertEqual((5, 409), variable.shape)
        self.assertEqual(DefaultData.get_default_fill_value(np.float32), variable.data[4, 307])
        self.assertEqual(DefaultData.get_default_fill_value(np.float32), variable.attrs["_FillValue"])
        self.assertEqual(standard_name, variable.attrs["standard_name"])
        self.assertEqual("K", variable.attrs["units"])

    def _assert_correct_refl_variable(self, variable, long_name):
        self.assertEqual((5, 409), variable.shape)
        self.assertEqual(DefaultData.get_default_fill_value(np.int16), variable.data[0, 8])
        self.assertEqual(DefaultData.get_default_fill_value(np.int16), variable.attrs["_FillValue"])
        self.assertEqual("toa_reflectance", variable.attrs["standard_name"])
        self.assertEqual(long_name, variable.attrs["long_name"])
        self.assertEqual(0.0, variable.attrs["add_offset"])
        self.assertEqual(1e-4, variable.attrs["scale_factor"])
        self.assertEqual("percent", variable.attrs["units"])
        self.assertEqual(15000, variable.attrs["valid_max"])
        self.assertEqual(0, variable.attrs["valid_min"])

    def _assert_correct_bt_variable(self, variable, long_name):
        self.assertEqual((5, 409), variable.shape)
        self.assertEqual(DefaultData.get_default_fill_value(np.int16), variable.data[0, 8])
        self.assertEqual(DefaultData.get_default_fill_value(np.int16), variable.attrs["_FillValue"])
        self.assertEqual("toa_brightness_temperature", variable.attrs["standard_name"])
        self.assertEqual(long_name, variable.attrs["long_name"])
        self.assertEqual(273.15, variable.attrs["add_offset"])
        self.assertEqual(0.01, variable.attrs["scale_factor"])
        self.assertEqual("K", variable.attrs["units"])
        self.assertEqual(10000, variable.attrs["valid_max"])
        self.assertEqual(-20000, variable.attrs["valid_min"])
