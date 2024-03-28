#ifndef ELECTRODE_H
#define ELECTRODE_H

#include <QObject>
#include <QRandomGenerator>

class Electrode : public QObject{
    Q_OBJECT
    
public:
    explicit Electrode(int site_number, QObject *parent = nullptr);
    ~Electrode();

private:
    int site_number_;
    void readFrequency(int site_number);

signals:
    void end();
    void send_frequency(float frequency);

private slots:
    void read_frequency(int site_number);
};

#endif // ELECTRODE_H
