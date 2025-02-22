//  START NUM TO WORDS
function numberToWords(num) {
    if (num === 0) return "nol";

    const birliklar = ["", "bir", "ikki", "uch", "to'rt", "besh", "olti", "yetti", "sakkiz", "to'qqiz"];
    const onliklar = ["", "o'n", "yigirma", "o'ttiz", "qirq", "ellik", "oltmish", "yetmish", "sakson", "to'qson"];

    function convertLessThanThousand(n) {
        let result = "";

        if (n >= 100) {
            result += birliklar[Math.floor(n / 100)] + " yuz ";
            n %= 100;
        }

        if (n >= 10) {
            result += onliklar[Math.floor(n / 10)] + " " + birliklar[n % 10] + " ";
        } else {
            result += birliklar[n] + " ";
        }

        return result.trim();
    }

    let result = "";

    if (num >= 1000000) {
        result += convertLessThanThousand(Math.floor(num / 1000000)) + " million ";
        num %= 1000000;
    }

    if (num >= 1000) {
        result += convertLessThanThousand(Math.floor(num / 1000)) + " ming ";
        num %= 1000;
    }

    result += convertLessThanThousand(num);

    return result.trim();
}

// END NUM TO WORDS


const app = Vue.createApp({
    data() {
        return {
            message: "Vue3 is working!",
            isValidated: false,
            created_by: null,
            doc: {
                "contract": {
                    "contract_number": "125-XMS",
                    "contract_date": "16.01.2025",
                    "credit_loan_total": null,
                    "credit_loan_total_word_uz": "",
                    "credit_start_date": "17.01.2027",
                    "credit_end_date": "16.01.2028",
                    "credit_percent": 60,
                    "credit_percent_word_uz": "",
                    "credit_term": 12,
                    "credit_term_word_uz": "",
                    "credit_graphic_type": "Annuitet",
                    "credit_type": "mikroqarz",
                }, "customer": {
                    "customer_passport_series": "AD",
                    "customer_passport_number": "1074617",
                    "customer_passport_pinfl": "31002873680015",
                    "customer_birthDate": "10.02.1987",
                    "customer_fullname": "",
                    "customer_fullname_initials": "",
                    "customer_document": "AD1074617",
                    "customer_issuedBy": "",
                    "customer_startDate": "",
                    "customer_address": "",
                    "customer_phone1": "+998 (93) 840-29-81",
                    "customer_phone2": "+995 (93) 840-29-81"
                }, "organization": {
                    "organization_title": "«CLEVER MIKROMOLIYA TASHKILOTI» MChJ",
                    "organization_address": "Toshkent shahri, Olmazor tumani, Sagbon ko'chasi, 30 boshi berk, 6-uy",
                    "organization_account_number": "20216000705068380001",
                    "organization_mfo": "01042",
                    "organization_stir": "306365847",
                    "organization_phone1": "+998 (93) 452-29-67",
                    "organization_phone2": "+998 (93) 656-56-81"
                }, "pledge": {
                    "pledge_is_owner": "yes",
                    "pledge_vehicle_TP_series": "AAG",
                    "pledge_vehicle_TP_number": "3371973",
                    "pledge_vehicleColor": "",
                    "pledge_issueYear": "",
                    "pledge_engineNumber": "",
                    "pledge_shassi": "Raqamsiz",
                    "pledge_vehicleTypeStr": "SEDAN",
                    "pledge_bodyNumber": "",
                    "pledge_govNumber": "01V940MC ",
                    "pledge_modelName": "",
                    "pledge_owner": "",
                    "pledge_loan_total": "",
                    "pledge_loan_total_word_uz": ""
                }, "branch": {
                    "branch_name_uz": "Xorazm viloyati Urganch filiali", "head_initials_uz": "Sharipov M.R."
                },
                "owner_data": {
                    "owner_passport_series": "AD",
                    "owner_passport_number": "0014687",
                    "owner_passport_pinfl": "40506963420023",
                    "owner_birthDate": "05.06.1996",
                    "owner_fullname": "",
                    "owner_fullname_initials": "",
                    "owner_document": "AD0014687",
                    "owner_issuedBy": "",
                    "owner_startDate": "",
                    "owner_address": "",
                },
                "config": {
                    "created_by": document.getElementById("app").dataset.initialValue,
                }
            }
        }
    },
    methods: {
        <!-- START GET PERSON V2-->
        get_person: function () {
            const validatebirthDate = this.doc.customer.customer_birthDate.split(".").reverse().join("-");
            const person_data = {
                "transactionId": Math.floor(Math.random() * 1000000),
                "isConsent": "Y",
                "senderPinfl": this.doc.customer.customer_passport_pinfl,
                "document": this.doc.customer.customer_document.toUpperCase(),
                "birthDate": validatebirthDate
            }
            console.log(person_data)
            const vp2 = this;
            const config = {
                headers: {Authorization: `Token 9ddf6eb7106bb6227171d914200148acc8e21675`}
            };
            axios.post('http://195.158.9.252:1441/passport_birth_date_v2/', person_data, config)
                .then(function (response) {
                    if (response.data.result) {
                        data = response.data.result;
                        console.log(data);
                        vp2.doc.customer.customer_passport_pinfl = data.pinfl;
                        vp2.doc.customer.customer_fullname = data.lastNameLatin + ' ' + data.firstNameLatin + ' ' + data.middleNameLatin;
                        vp2.doc.customer.customer_address = data.address;
                        vp2.doc.customer.customer_issuedBy = data.issuedBy;
                        vp2.doc.customer.customer_startDate = data.startDate.split("-").reverse().join(".");
                        vp2.doc.customer.customer_fullname_initials = data.firstNameLatin[0] + '.' + data.middleNameLatin[0] + '.' + data.lastNameLatin;

                    } else {
                        console.log("No data")
                    }
                })
                .catch(function (error) {
                    alert('V2 Passport malumotlari serverida xatolik');
                    console.log(error);
                });
        },
        <!-- END GET PERSON -->

        <!-- START GET OWNER V2-->
        get_owner: function () {
            const validatebirthDate = this.doc.owner_data.owner_birthDate.split(".").reverse().join("-");
            const owner_data = {
                "transactionId": Math.floor(Math.random() * 1000000),
                "isConsent": "Y",
                "senderPinfl": this.doc.owner_data.owner_passport_pinfl,
                "document": this.doc.owner_data.owner_document.toUpperCase(),
                "birthDate": validatebirthDate
            }
            console.log(owner_data)
            const ow = this;
            const config = {
                headers: {Authorization: `Token 9ddf6eb7106bb6227171d914200148acc8e21675`}
            };
            axios.post('http://195.158.9.252:1441/passport_birth_date_v2/', owner_data, config)
                .then(function (response) {
                    if (response.data.result) {
                        data = response.data.result;
                        console.log(data);
                        ow.doc.owner_data.owner_passport_pinfl = data.pinfl;
                        ow.doc.owner_data.owner_fullname = data.lastNameLatin + ' ' + data.firstNameLatin + ' ' + data.middleNameLatin;
                        ow.doc.owner_data.owner_address = data.address;
                        ow.doc.owner_data.owner_issuedBy = data.issuedBy;
                        ow.doc.owner_data.owner_startDate = data.startDate.split("-").reverse().join(".");
                        ow.doc.owner_data.owner_fullname_initials = data.firstNameLatin[0] + '.' + data.middleNameLatin[0] + '.' + data.lastNameLatin;

                    } else {
                        console.log("No data")
                    }
                })
                .catch(function (error) {
                    alert('V2 Passport malumotlari serverida xatolik');
                    console.log(error);
                });
        },
        <!-- END GET OWNER -->

        <!-- START GET PERSON V2-->
        get_vehicle: function () {
            const vehicle_data =
                {
                    "techPassportSeria": this.doc.pledge.pledge_vehicle_TP_series.toUpperCase(),
                    "techPassportNumber": this.doc.pledge.pledge_vehicle_TP_number,
                    "govNumber": this.doc.pledge.pledge_govNumber
                }

            console.log(vehicle_data)
            const vp3 = this;
            const config = {
                headers: {Authorization: `Token 9ddf6eb7106bb6227171d914200148acc8e21675`}
            };
            axios.post('http://195.158.9.252:1441/vehicle/', vehicle_data, config)
                .then(function (response) {
                    if (response.data.result) {
                        data = response.data.result;
                        console.log(data);
                        vp3.doc.pledge.pledge_modelName = data.modelName;
                        vp3.doc.pledge.pledge_bodyNumber = data.bodyNumber;
                        vp3.doc.pledge.pledge_engineNumber = data.engineNumber;
                        vp3.doc.pledge.pledge_issueYear = data.issueYear;
                        vp3.doc.pledge.pledge_owner = data.owner;
                        vp3.doc.pledge.pledge_vehicleColor = data.vehicleColor;
                    } else {
                        console.log("No data")
                    }
                })
                .catch(function (error) {
                    alert('Transport malumotlari topilmadi');
                    console.log(error);
                });
        },
        <!-- END GET PERSON -->

        handleNum2Word() {
            const credit_loan_total = Number(this.doc.contract.credit_loan_total.trim().replace(/\s+/g, ""));
            this.doc.contract.credit_loan_total_word_uz = numberToWords(credit_loan_total);
            this.doc.contract.credit_percent_word_uz = numberToWords(Number(this.doc.contract.credit_percent));
            this.doc.contract.credit_term_word_uz = numberToWords(Number(this.doc.contract.credit_term));

            const pledge_loan_total = Number(this.doc.pledge.pledge_loan_total.trim().replace(/\s+/g, ""));

            this.doc.pledge.pledge_loan_total_word_uz = numberToWords(pledge_loan_total);
        },

        validateForm() {
            let form = this.$refs.myForm; // Formani olish
            if (form.checkValidity()) {
                alert("Forma to‘g‘ri to‘ldirildi ✅");
                // Shu yerda formani jo‘natish yoki boshqa harakat qilish mumkin
                this.createContract(this.doc)
            } else {
                this.isValidated = true; // Xatolarni ko‘rsatish uchun Bootstrap klassini qo‘shish
            }
        },

        //     CreateContract
        createContract: function (doc) {
            const csrftoken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

            axios.post('http://127.0.0.1:8000/contract/create_contract/', doc, {
                headers: {
                    'X-CSRFToken': csrftoken
                }
            })
                .then(function (response) {
                    if (response) {
                        console.log(response.data);
                        window.location.href = '/contract/mikroqarz_list/';

                    } else {
                        console.log("No data")
                    }
                })
                .catch(function (error) {
                    alert('Serverida xatolik');
                    console.log(error);
                });
        }
    },
    mounted() {
        Inputmask("+998 (99) 999-99-99").mask("#customer_phone1");

        // Telefon raqami maskasi
        Inputmask("+998 (99) 999-99-99").mask("#customer_phone1");

        // Telefon raqami maskasi
        Inputmask("+998 (99) 999-99-99").mask("#customer_phone2");

        // Sana (kun/oy/yil) maskasi
        Inputmask("99.99.9999", {placeholder: "DD.MM.YYYY"}).mask("#contract_date");

        // Sana (kun/oy/yil) maskasi
        Inputmask("99.99.9999", {placeholder: "DD.MM.YYYY"}).mask("#credit_start_date");

        // Sana (kun/oy/yil) maskasi
        Inputmask("99.99.9999", {placeholder: "DD.MM.YYYY"}).mask("#credit_end_date");

        // Raqam (pul miqdori) maskasi
        Inputmask({
            alias: "numeric",
            groupSeparator: " ",
            autoGroup: true,
            digits: 2,
            radixPoint: ".",
            rightAlign: false
        }).mask("#credit_loan_total");

        // customer_document maskasi
        Inputmask("AA9999999").mask("#customer_document");

        // customer_passport_pinfl maskasi
        Inputmask("99999999999999").mask("#customer_passport_pinfl");

        // customer_birthDate (kun/oy/yil) maskasi
        Inputmask("99.99.9999", {placeholder: "DD.MM.YYYY"}).mask("#customer_birthDate");

        // pledge_vehicle_TP_series maskasi
        Inputmask("AAA", {placeholder: "AAG"}).mask("#pledge_vehicle_TP_series");

        // pledge_vehicle_TP_number maskasi
        Inputmask("9999999", {placeholder: "1234567"}).mask("#pledge_vehicle_TP_number");

        // pledge_vehicle_TP_number maskasi
        Inputmask("9999999", {placeholder: "AAG"}).mask("#pledge_vehicle_TP_number");

        // pledge_loan_total (pul miqdori) maskasi
        Inputmask({
            alias: "numeric",
            groupSeparator: " ",
            autoGroup: true,
            digits: 2,
            radixPoint: ".",
            rightAlign: false
        }).mask("#pledge_loan_total");
    }
})


// Delimiters changed to ES6 template string style
app.config.compilerOptions.delimiters = ['[[', ']]']

app.mount('#app')