#include <lmic.h>
#include <hal/hal.h>
#include <SPI.h>
#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>
#include <Wire.h>

Adafruit_MPU6050 mpu;

void os_getArtEui (u1_t* buf) { }
void os_getDevEui (u1_t* buf) { }
void os_getDevKey (u1_t* buf) { }

static osjob_t sendjob;

const lmic_pinmap lmic_pins = {
    .nss = 10,
    .rxtx = LMIC_UNUSED_PIN,
    .rst = 8,
    .dio = {6, 6, 6},
};

void onEvent (ev_t ev) {
    switch(ev) {
        case EV_TXCOMPLETE:
            Serial.println(F("EV_TXCOMPLETE"));
            os_setTimedCallback(&sendjob, os_getTime()+sec2osticks(15), do_send);
            break;
    }
}

void do_send(osjob_t* j){
    sensors_event_t a, g, temp;
    mpu.getEvent(&a, &g, &temp);
    
    uint8_t payload[12];
    
    memcpy(payload, &a.acceleration.x, sizeof(float));
    memcpy(payload + 4, &a.acceleration.y, sizeof(float));
    memcpy(payload + 8, &a.acceleration.z, sizeof(float));
    
    // Send data
    if (LMIC.opmode & OP_TXRXPEND) {
        return;
    } else {
        LMIC_setTxData2(1, payload, sizeof(payload), 0);
        Serial.println(F("Packet queued"));
    }
}

void setup() {

    if (!mpu.begin()) {
      Serial.println("Failed to find MPU6050 chip");
      while (1) {
        delay(10);
      }
    }
    Serial.println("MPU6050 Found!");
    mpu.setAccelerometerRange(MPU6050_RANGE_8_G);
    mpu.setGyroRange(MPU6050_RANGE_500_DEG);
    mpu.setFilterBandwidth(MPU6050_BAND_21_HZ);
    delay(100);

    static const u4_t DEVADDR = 0x01DF4759;
    static const PROGMEM u1_t NWKSKEY[16] = {0x1C, 0xA5, 0x36, 0x0E, 0xE0, 0x6C, 0xAC, 0x7F, 0xF8, 0x4A, 0xB2, 0xC1, 0x8C, 0x11, 0x48, 0x60};
    static const u1_t PROGMEM APPSKEY[16] = {0x44, 0x86, 0x93, 0x82, 0x2D, 0x2F, 0xF6, 0x53, 0x5C, 0xB2, 0x76, 0xDB, 0x9E, 0x83, 0x8D, 0x30};


    Serial.begin(115200);
    os_init();
    LMIC_reset();
    LMIC_setClockError(MAX_CLOCK_ERROR * 2 / 100);

    #ifdef PROGMEM
    uint8_t appskey[sizeof(APPSKEY)];
    uint8_t nwkskey[sizeof(NWKSKEY)];
    memcpy_P(appskey, APPSKEY, sizeof(APPSKEY));
    memcpy_P(nwkskey, NWKSKEY, sizeof(NWKSKEY));
    LMIC_setSession (0x1, DEVADDR, nwkskey, appskey);
    #else
    LMIC_setSession (0x1, DEVADDR, NWKSKEY, APPSKEY);
    #endif
 
    LMIC_setupChannel(0, 921400000, DR_RANGE_MAP(DR_SF12, DR_SF7),  BAND_CENTI);     
    LMIC_setupChannel(1, 921600000, DR_RANGE_MAP(DR_SF12, DR_SF7B), BAND_CENTI);
    LMIC_setupChannel(2, 921800000, DR_RANGE_MAP(DR_SF12, DR_SF7),  BAND_CENTI);
    LMIC_setupChannel(3, 922000000, DR_RANGE_MAP(DR_SF12, DR_SF7),  BAND_CENTI);
    LMIC_setupChannel(4, 922200000, DR_RANGE_MAP(DR_SF12, DR_SF7),  BAND_CENTI);
    LMIC_setupChannel(5, 922400000, DR_RANGE_MAP(DR_SF12, DR_SF7),  BAND_CENTI);
    LMIC_setupChannel(6, 922600000, DR_RANGE_MAP(DR_SF12, DR_SF7),  BAND_CENTI);
    LMIC_setupChannel(7, 922800000, DR_RANGE_MAP(DR_SF12, DR_SF7),  BAND_CENTI);
    LMIC_setupChannel(8, 922700000, DR_RANGE_MAP(DR_FSK,  DR_FSK),  BAND_MILLI);

    LMIC_setLinkCheckMode(0);

    LMIC.dn2Dr = DR_SF9;

    LMIC_setDrTxpow(DR_SF7,14);

    do_send(&sendjob);
}

void loop() {
    os_runloop_once();
}
