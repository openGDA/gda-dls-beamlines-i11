package uk.ac.gda.beamline.i11.views;
/*-
 * Copyright © 2011 Diamond Light Source Ltd.
 *
 * This file is part of GDA.
 *
 * GDA is free software: you can redistribute it and/or modify it under the
 * terms of the GNU General Public License version 3 as published by the Free
 * Software Foundation.
 *
 * GDA is distributed in the hope that it will be useful, but WITHOUT ANY
 * WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
 * FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
 * details.
 *
 * You should have received a copy of the GNU General Public License along
 * with GDA. If not, see <http://www.gnu.org/licenses/>.
 */

import gda.device.CurrentAmplifier;
import gda.device.CurrentAmplifier.Status;
import gda.device.DeviceException;
import gda.observable.IObserver;
import gda.rcp.views.CompositeFactory;

import org.eclipse.jface.layout.GridDataFactory;
import org.eclipse.jface.layout.GridLayoutFactory;
import org.eclipse.swt.SWT;
import org.eclipse.swt.events.PaintEvent;
import org.eclipse.swt.events.PaintListener;
import org.eclipse.swt.graphics.Color;
import org.eclipse.swt.graphics.GC;
import org.eclipse.swt.graphics.Point;
import org.eclipse.swt.graphics.Rectangle;
import org.eclipse.swt.layout.GridData;
import org.eclipse.swt.widgets.Canvas;
import org.eclipse.swt.widgets.Composite;
import org.eclipse.swt.widgets.Display;
import org.eclipse.swt.widgets.Group;
import org.eclipse.ui.IWorkbenchPartSite;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class BeamStatusCompositeFactory implements CompositeFactory {
	
	static final Logger logger = LoggerFactory.getLogger(BeamStatusCompositeFactory.class);
	
	private String label;
	private CurrentAmplifier curramp;
	private double threshold;

	public String getLabel() {
		return label;
	}

	public void setLabel(String label) {
		this.label = label;
	}

	@Override
	public Composite createComposite(Composite parent, int style, IWorkbenchPartSite iWorkbenchPartSite) {
		return new BeamStatusComposite(parent, style, iWorkbenchPartSite.getShell().getDisplay(), label, curramp, threshold);
	}

	public CurrentAmplifier getCurramp() {
		return curramp;
	}

	public void setCurramp(CurrentAmplifier curramp) {
		this.curramp = curramp;
	}

	public double getThreshold() {
		return threshold;
	}

	public void setThreshold(double threshold) {
		this.threshold = threshold;
	}
}

class BeamStatusComposite extends Composite {
	private static final Logger logger = LoggerFactory.getLogger(BeamStatusComposite.class);
	
	private final Color BEAM_ON_COLOR = Display.getDefault().getSystemColor(SWT.COLOR_GREEN);
	private final Color BEAM_OVERLOAD_COLOR = Display.getDefault().getSystemColor(SWT.COLOR_YELLOW);
	private final Color BEAM_OFF_COLOR = Display.getDefault().getSystemColor(SWT.COLOR_RED);
	
	private Display display;
	private Color currentColor;
	private Canvas beamCanvas;
	private BeamStatus beamStatus=BeamStatus.ON;
	
	private CurrentAmplifier curramp;
	public CurrentAmplifier getCurramp() {
		return curramp;
	}

	public void setCurramp(CurrentAmplifier curramp) {
		this.curramp = curramp;
	}

	private double threshold;

	public double getThreshold() {
		return threshold;
	}

	public void setThreshold(double threshold) {
		this.threshold = threshold;
	}

	/**
	 * defines the overload status of the amplifier
	 * 
	 * @author fy65
	 */
	public enum BeamStatus {
		/**
		 * Ion Chamber Amplifier indicates Beam on
		 */
		ON,
		/**
		 * Ion Chamber Amplifier indicates Beam off
		 */
		OFF,
		/**
		 * Ion Chamber Amplifier indicates measurement overload
		 */
		OVERLOADED;
		/**
		 * converts value to Status
		 * 
		 * @param value
		 * @return status
		 */
		public static BeamStatus from_int(int value) {
			BeamStatus s = BeamStatus.ON;
			switch (value) {
			case 0:
				s = BeamStatus.ON;
				break;
			case 1:
				s = BeamStatus.OFF;
				break;
			case 2:
				s = BeamStatus.OVERLOADED;
				break;
			default:
				s = BeamStatus.ON;
			}
			return s;

		}
	}
	
	public boolean isBeamOn() {
		return beamStatus == BeamStatus.ON;
	}

	public void setBeamOn(BeamStatus beamOn) {
		this.beamStatus = beamOn;
	}

	public BeamStatusComposite(Composite parent, int style, final Display display, String label, CurrentAmplifier curramp, double threshold) {
		super(parent, style);

		GridDataFactory.fillDefaults().applyTo(this);
		GridLayoutFactory.swtDefaults().numColumns(1).applyTo(this);
		
		Group grp = new Group(this, style);
		GridDataFactory.fillDefaults().applyTo(grp);
		GridLayoutFactory.swtDefaults().numColumns(1).applyTo(grp);
		grp.setText(label);

		this.display = display;
		GridLayoutFactory.swtDefaults().numColumns(1).applyTo(this);
		GridDataFactory.fillDefaults().applyTo(this);
		
		this.curramp=curramp;
		this.threshold=threshold;
		
		double curval = 0.0;
		Status status = Status.NORMAL;
		try {
			curval = curramp.getCurrent();
			status = curramp.getStatus();
		} catch (DeviceException e) {
			logger.warn("Cannot get current value from apmlifier {}", curramp.getName());
		}
		
		currentColor = BEAM_OFF_COLOR;
		
		if (curval > threshold) {
			beamStatus = BeamStatus.ON;
			currentColor=BEAM_ON_COLOR;
		} else {
			beamStatus = BeamStatus.OFF;
			currentColor=BEAM_OFF_COLOR;
		}
		if (status == Status.OVERLOAD) {
			beamStatus = BeamStatus.OVERLOADED;
			currentColor=BEAM_OVERLOAD_COLOR;
		}

		beamCanvas = new Canvas(grp, SWT.NONE);
		GridData gridData = new GridData(GridData.VERTICAL_ALIGN_FILL);
		gridData.widthHint = 40;
		gridData.heightHint = 40;
		beamCanvas.setLayoutData(gridData);
		beamCanvas.addPaintListener(new PaintListener() {
			@Override
			public void paintControl(PaintEvent e) {
				GC gc = e.gc;
				gc.setAntialias(SWT.ON);
				gc.setBackground(currentColor);
				gc.setLineWidth(1);
				Rectangle clientArea = beamCanvas.getClientArea();
				final int margin = 4;
				final Point topLeft = new Point(margin, margin);
				final Point size = new Point(clientArea.width - margin * 2, clientArea.height - margin * 2);
				gc.fillOval(topLeft.x, topLeft.y, size.x, size.y);
				gc.drawOval(topLeft.x, topLeft.y, size.x, size.y);
			}
		});
		
		final IObserver beamObserver = new IObserver() {
			@Override
			public void update(final Object theObserved, final Object changeCode) {
				Display.getDefault().asyncExec(new Runnable() {
					@Override
					public void run() {
						double value = -999;
						if (theObserved instanceof CurrentAmplifier) {
							if (changeCode instanceof Double) {
								value = Math.abs(((Double) changeCode).doubleValue());
								if (value <= getThreshold()) {
									if (beamStatus != BeamStatus.OFF) {
										beamStatus = BeamStatus.OFF;
										currentColor=BEAM_OFF_COLOR;
									}
								} else {
									if (beamStatus != BeamStatus.ON) {
										beamStatus = BeamStatus.ON;
										currentColor=BEAM_ON_COLOR;
									}
								}
							} else if (changeCode instanceof CurrentAmplifier.Status) {
								CurrentAmplifier.Status status = (CurrentAmplifier.Status) changeCode;
								if (status == CurrentAmplifier.Status.OVERLOAD) {
									if (beamStatus != BeamStatus.OVERLOADED) {
										beamStatus = BeamStatus.OVERLOADED;
										currentColor=BEAM_OVERLOAD_COLOR;
									}
								}
							}
						}
						updateBatonCanvas();
						
					}
				});
			}
		};

		curramp.addIObserver(beamObserver);
	}

	private void updateBatonCanvas() {
		display.asyncExec(new Runnable() {
			
			@Override
			public void run() {
				beamCanvas.redraw();
				beamCanvas.update();
			}
		});
	}
	
	@Override
	public void dispose() {
		super.dispose();
	}
}
