package org.opengda.lde.ui.providers;

import java.text.DateFormat;
import java.util.Calendar;
import java.util.Date;

import org.eclipse.draw2d.ColorConstants;
import org.eclipse.jface.viewers.ITableColorProvider;
import org.eclipse.jface.viewers.ITableLabelProvider;
import org.eclipse.jface.viewers.LabelProvider;
import org.eclipse.swt.graphics.Color;
import org.eclipse.swt.graphics.Image;
import org.opengda.lde.model.ldeexperiment.STATUS;
import org.opengda.lde.model.ldeexperiment.Sample;
import org.opengda.lde.ui.Activator;
import org.opengda.lde.ui.ImageConstants;

public class SampleGroupViewLabelProvider extends LabelProvider implements ITableLabelProvider, ITableColorProvider {

	@Override
	public Color getForeground(Object element, int columnIndex) {
		if (columnIndex == SampleTableConstants.COL_STATUS) {
			return ColorConstants.red;
		}
		return null;
	}

	@Override
	public Color getBackground(Object element, int columnIndex) {
		if (columnIndex == SampleTableConstants.COL_STATUS) {
			return ColorConstants.white;
		}
		return null;
	}

	@Override
	public Image getColumnImage(Object element, int columnIndex) {
		if (element instanceof Sample) {
			Sample sample = (Sample) element;
			if (columnIndex == SampleTableConstants.COL_ACTIVE) {
				//TODO replace with check box 
				if (sample.isActive()) {
					return Activator.getDefault().getImageRegistry().get(ImageConstants.ICON_CHECKED_STATE);
				} else {
					return Activator.getDefault().getImageRegistry().get(ImageConstants.ICON_UNCHECKED_STATE);
				}
			} else if (columnIndex == SampleTableConstants.COL_STATUS) {
				if (sample.isActive()) {
					if (sample.getStatus() == STATUS.READY) {
						return Activator.getDefault().getImageRegistry().get(ImageConstants.ICON_RUN_READY);
					} else if (sample.getStatus() == STATUS.RUNNING) {
						return Activator.getDefault().getImageRegistry().get(ImageConstants.ICON_RUNNING);
					} else if (sample.getStatus() == STATUS.COMPLETED) {
						return Activator.getDefault().getImageRegistry().get(ImageConstants.ICON_RUN_COMPLETE);
					} else if (sample.getStatus() == STATUS.ABORTED) {
						return Activator.getDefault().getImageRegistry().get(ImageConstants.ICON_RUN_FAILURE);
					} else if (sample.getStatus() == STATUS.ERROR) {
						return Activator.getDefault().getImageRegistry().get(ImageConstants.ICON_ERROR);
					}
				}
			}
		}
		return null;
	}

	@Override
	public String getColumnText(Object element, int columnIndex) {
		if (element instanceof Sample) {
			Sample sample = (Sample) element;
			switch (columnIndex) {
			case SampleTableConstants.COL_STATUS:
				return "";

			case SampleTableConstants.COL_ACTIVE:
				return "";
			case SampleTableConstants.COL_SAMPLE_NAME:
				return sample.getName();
			case SampleTableConstants.COL_CELL_ID:
				return sample.getCellID();
			case SampleTableConstants.COL_VISIT_ID:
				return sample.getVisitID();
			case SampleTableConstants.COL_CALIBRANT_NAME:
				return sample.getCalibrant();
			case SampleTableConstants.COL_EMAIL:
				return sample.getEmail();
			case SampleTableConstants.COL_COMMAND:
				return sample.getCommand();
			case SampleTableConstants.COL_COMMENT:
				return sample.getComment();
			case SampleTableConstants.COL_START_DATE:
				if (sample.getStartDate()!= null ){
					return DateFormat.getInstance().format(sample.getStartDate());
				}
				return DateFormat.getInstance().format(new Date());
			case SampleTableConstants.COL_END_DATE:
				if (sample.getEndDate()!= null){
					return DateFormat.getInstance().format(sample.getEndDate());
				} 
				return DateFormat.getInstance().format(new Date());
			case SampleTableConstants.COL_MAIL_COUNT:
				return Integer.toString(sample.getMailCount());
			case SampleTableConstants.COL_DATA_FILE_COUNT:
				return Integer.toString(sample.getDataFileCount());
			}
		}
		return null;

	}
}
