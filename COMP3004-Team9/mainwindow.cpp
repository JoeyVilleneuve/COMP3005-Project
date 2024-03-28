#include "mainwindow.h"
#include "ui_mainwindow.h"

MainWindow::MainWindow(QWidget *parent) : QMainWindow(parent), ui(new Ui::MainWindow){
    ui->setupUi(this);
    neureset_ = new NeuresetDevice();

    // Setup signals & slots
    connect(this, SIGNAL(button_start_session()), neureset_, SLOT(button_start_session()));
}

MainWindow::~MainWindow(){
    delete ui;
}

// Signals & slots
void MainWindow::on_start_session_clicked(){ emit(button_start_session()); }
