#include "electrode.h"

Electrode::Electrode(int site_number, QObject *parent) : QObject{parent}{
    site_number_ = site_number;
}

Electrode::~Electrode(){ emit end(); }

void Electrode::readFrequency(int site_number){
    if (site_number_ != site_number) { return; } // Only read if this is the target site
    QRandomGenerator* random_generator = QRandomGenerator::global();
    float frequency = random_generator->generateDouble() * 35; // Random float between 0-35hz
    emit(send_frequency(frequency));
}

// Signals & slots
void Electrode::read_frequency(int site_number){ readFrequency(site_number); }
