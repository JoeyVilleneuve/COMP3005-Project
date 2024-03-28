#include "eegheadset.h"

EEGHeadset::EEGHeadset(QObject *parent) : QObject{parent}{
    num_electrodes_ = 21;

    // Start new thread for each electrode
    for(int i = 0; i < num_electrodes_; i++){
        QThread* thread = new QThread();
        Electrode* electrode = new Electrode(i+1);
        electrode->moveToThread(thread);

        // Setup signals & slots
        connect(electrode, &Electrode::end, thread, &QThread::quit);
        connect(electrode, &Electrode::end, electrode, &Electrode::deleteLater);
        connect(thread, &QThread::finished, thread, &QThread::deleteLater);

        connect(this, SIGNAL(electrode_read_frequency(int)), electrode, SLOT(read_frequency(int)));
        connect(electrode, SIGNAL(send_frequency(float)), this, SLOT(receive_frequency(float)));

        thread->start();
    }
}

int EEGHeadset::numElectrodes() { return num_electrodes_; }

void EEGHeadset::delay(int milliseconds){
    QTimer timer;
    timer.setInterval(milliseconds);
    QEventLoop loop;
    connect(&timer, SIGNAL(timeout()), &loop, SLOT(quit()));
    timer.start();
    loop.exec();
}

float EEGHeadset::readFrequency(int site_number){
    emit(electrode_read_frequency(site_number));
    while(true){ // Wait for return signal
        if(frequency_buffer_.size() > 0){
            return frequency_buffer_[0];
        }
    }
}

float EEGHeadset::readBaseline(int site_number){
    for(int i = 0; i < 2; i++){ // Scan site every 1 sec for 1 min
        emit(electrode_read_frequency(site_number));
        delay(1000);
    }

    // Calculate baseline average
    float avg = 0;
    for(int i = 0; i < frequency_buffer_.size(); i++){
        avg += frequency_buffer_[i];
    }
    avg /= frequency_buffer_.size();
    frequency_buffer_.clear();
    return avg;
}

float EEGHeadset::deliver_treatment(int site_number, float baseline_average){
    float frequency = baseline_average;
    for(int i = 0; i < 16; i++){ // Add 5hz offset and recalculate frequency every 1/16 sec for 1 sec
        frequency += 5.0;
        delay(63);
    }
    return frequency;
}

// Signals & slots
float EEGHeadset::read_frequency(int site_number){ return readFrequency(site_number); }
float EEGHeadset::read_baseline(int site_number){ return readBaseline(site_number); }
void EEGHeadset::receive_frequency(float frequency){ frequency_buffer_.push_back(frequency); }
