package org.opengda.lde.ui.providers;

public interface SampleTableConstants {

	final static int COL_STATUS = 0;
	static final int COL_ACTIVE = COL_STATUS + 1;
	static final int COL_SAMPLE_NAME = COL_ACTIVE + 1;
	static final int COL_CELL_ID = COL_SAMPLE_NAME + 1;
	static final int COL_VISIT_ID = COL_CELL_ID + 1;
	static final int COL_CALIBRANT_NAME= COL_VISIT_ID + 1;
	static final int COL_CALIBRANT_X= COL_CALIBRANT_NAME + 1;
	static final int COL_CALIBRANT_Y= COL_CALIBRANT_X + 1;
	static final int COL_CALIBRANT_EXPOSURE= COL_CALIBRANT_Y + 1;
	static final int COL_SAMPLE_X_START= COL_CALIBRANT_EXPOSURE + 1;
	static final int COL_SAMPLE_X_STOP= COL_SAMPLE_X_START + 1;
	static final int COL_SAMPLE_X_STEP= COL_SAMPLE_X_STOP + 1;
	static final int COL_SAMPLE_Y_START= COL_SAMPLE_X_STEP + 1;
	static final int COL_SAMPLE_Y_STOP= COL_SAMPLE_Y_START + 1;
	static final int COL_SAMPLE_Y_STEP= COL_SAMPLE_Y_STOP + 1;
	static final int COL_SAMPLE_EXPOSURE= COL_SAMPLE_Y_STEP + 1;
	static final int COL_DETECTOR_X= COL_SAMPLE_EXPOSURE + 1;
	static final int COL_DETECTOR_Y= COL_DETECTOR_X + 1;
	static final int COL_DETECTOR_Z= COL_DETECTOR_Y + 1;
	static final int COL_EMAIL = COL_DETECTOR_Z + 1;
	static final int COL_START_DATE = COL_EMAIL + 1;
	static final int COL_END_DATE = COL_START_DATE + 1;
	static final int COL_COMMAND = COL_END_DATE + 1;
	static final int COL_MAIL_COUNT = COL_COMMAND + 1;
	static final int COL_DATA_FILE_COUNT = COL_MAIL_COUNT + 1;
	static final int COL_COMMENT = COL_DATA_FILE_COUNT + 1;

	static final String STATUS = "Status";
	static final String ACTIVE = "Active";
	static final String SAMPLE_NAME = "Sample Name";
	static final String CELL_ID = "Cell ID";
	static final String VISIT_ID = "Visit ID";
	static final String CALIBRANT_NAME = "Calibrant";
	static final String CALIBRANT_X = "Calibrant X";
	static final String CALIBRANT_Y = "Calibrant Y";
	static final String CALIBRANT_EXPOSURE = "Calibrant Exposure";
	static final String SAMPLE_X_START= "Sample X_Start";
	static final String SAMPLE_X_STOP= "Sample X_Stop";
	static final String SAMPLE_X_STEP= "Sample X_Step";
	static final String SAMPLE_Y_START= "Sample Y_Start";
	static final String SAMPLE_Y_STOP= "Sample Y_Stop";
	static final String SAMPLE_Y_STEP= "Sample Y_Step";
	static final String SAMPLE_EXPOSURE= "Sample Exposure";
	static final String DETECTOR_X= "Detector X";
	static final String DETECTOR_Y= "Detector Y";
	static final String DETECTOR_Z= "Detector Z";
	static final String EMAIL = "Email";
	static final String START_DATE = "Start Date";
	static final String END_DATE = "End Date";
	static final String COMMAND = "Command";
	static final String MAIL_COUNT = "Mail Count";
	static final String DATA_FILE_COUNT = "Data Count";
	static final String COMMENT = "Comment";
}
