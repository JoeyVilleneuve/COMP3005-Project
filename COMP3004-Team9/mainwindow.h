#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include <neuresetdevice.h>

QT_BEGIN_NAMESPACE
namespace Ui { class MainWindow; }
QT_END_NAMESPACE

class MainWindow : public QMainWindow{
    Q_OBJECT

public:
    MainWindow(QWidget *parent = nullptr);
    ~MainWindow();

private:
    Ui::MainWindow* ui;
    NeuresetDevice* neureset_;

signals:
    void button_start_session();

private slots:
    void on_start_session_clicked();
};
#endif // MAINWINDOW_H
