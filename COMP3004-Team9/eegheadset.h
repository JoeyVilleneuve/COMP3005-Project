#ifndef EEGHEADSET_H
#define EEGHEADSET_H

#include <electrode.h>
#include <QObject>
#include <QVector>
#include <QThread>
#include <QTimer>
#include <QEventLoop>
#include <QDebug>

class EEGHeadset : public QObject { 
    Q_OBJECT

public:
    explicit EEGHeadset(QObject *parent = nullptr);
    int numElectrodes();

private:
    QVector<Electrode*> electrodes_;
    QVector<float> frequency_buffer_;
    int num_electrodes_;
    void delay(int milliseconds);
    float readFrequency(int site_number);
    float readBaseline(int site_number);

signals:
    void electrode_read_frequency(int site_number);

private slots:
    // NeuresetDevice
    float read_frequency(int site_number);
    float read_baseline(int site_number);
    float deliver_treatment(int site_number, float baseline_average);
    // Electrode
    void receive_frequency(float frequency);
};

#endif // EEGHEADSET_H
