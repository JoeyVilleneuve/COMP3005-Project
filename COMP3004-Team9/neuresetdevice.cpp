#include "neuresetdevice.h"

NeuresetDevice::NeuresetDevice(QObject *parent) : QObject{parent}{
    headset_ = new EEGHeadset();

    // Setup signals & slots
    connect(this, SIGNAL(headset_read_baseline(int)), headset_, SLOT(read_baseline(int)));
    connect(this, SIGNAL(headset_deliver_treatment(int, float)), headset_, SLOT(deliver_treatment(int, float)));
}

void NeuresetDevice::delay(int milliseconds){
    QTimer timer;
    timer.setInterval(milliseconds);
    QEventLoop loop;
    connect(&timer, SIGNAL(timeout()), &loop, SLOT(quit()));
    timer.start();
    loop.exec();
}

void NeuresetDevice::startSession(){
    qDebug() << "Starting session...";

    for(int i = 0; i < headset_->numElectrodes(); i++){ // At each site...

        // Establish baseline average (1 min)
        float avg = emit(headset_read_baseline(i+1));
        qDebug() << "Site" << i+1 << "baseline:" << avg;

        // Deliver treatment (1 sec)
        float frequency = emit(headset_deliver_treatment(i+1, avg));
        qDebug() << "Site" << i+1 << "after treatment frequency:" << frequency;
    }
}

// Signals & slots
void NeuresetDevice::button_start_session(){ startSession(); }
