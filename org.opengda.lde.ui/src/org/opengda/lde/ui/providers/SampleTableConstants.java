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

	static final String STATUS = "Run\nState";
	static final String ACTIVE = "Use";
	static final String SAMPLE_NAME = "Sample\nName";
	static final String CELL_ID = "Cell\nID";
	static final String VISIT_ID = "Visit\nID";
	static final String CALIBRANT_NAME = "Calibrant";
	static final String CALIBRANT_X = "Calibrant\nX";
	static final String CALIBRANT_Y = "Calibrant\nY";
	static final String CALIBRANT_EXPOSURE = "Calibrant\nExposure";
	static final String SAMPLE_X_START= "Sample\nX Start";
	static final String SAMPLE_X_STOP= "Sample\nX Stop";
	static final String SAMPLE_X_STEP= "Sample\nX Step";
	static final String SAMPLE_Y_START= "Sample\nY Start";
	static final String SAMPLE_Y_STOP= "Sample\nY Stop";
	static final String SAMPLE_Y_STEP= "Sample\nY Step";
	static final String SAMPLE_EXPOSURE= "Sample\nExposure";
	static final String DETECTOR_X= "Detector\nX";
	static final String DETECTOR_Y= "Detector\nY";
	static final String DETECTOR_Z= "Detector\nZ";
	static final String EMAIL = "Email";
	static final String START_DATE = "Start Date";
	static final String END_DATE = "End Date";
	static final String COMMAND = "Command";
	static final String MAIL_COUNT = "Mail\nCount";
	static final String DATA_FILE_COUNT = "Data\nCount";
	static final String COMMENT = "Comment";
}
