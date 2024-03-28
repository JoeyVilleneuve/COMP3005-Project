#ifndef NEURESETDEVICE_H
#define NEURESETDEVICE_H

#include <QObject>
#include <eegheadset.h>

class NeuresetDevice : public QObject{
    Q_OBJECT

public:
    explicit NeuresetDevice(QObject *parent = nullptr);
    void startSession();

private:
    EEGHeadset* headset_;
    void delay(int milliseconds);
    
signals:
    float headset_read_baseline(int site_number);
    float headset_deliver_treatment(int site_number, float baseline_average);

private slots:
    // MainWindow
    void button_start_session();
    // EEGHeadset
};

#endif // NEURESETDEVICE_H
