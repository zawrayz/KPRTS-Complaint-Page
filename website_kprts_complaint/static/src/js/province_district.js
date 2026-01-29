console.log("✅ KPRTS frontend dependency JS loaded");

/* =================================
   PROVINCE → DISTRICT (DELEGATED)
================================= */
document.addEventListener("change", function (e) {
    if (e.target && e.target.id === "province_select") {
        const province = e.target.value;
        const districtSelect = document.getElementById("district_select");

        if (!districtSelect) return;

        const districtsByProvince = {
            punjab: [
                { value: "lahore", label: "Lahore" },
                { value: "rawalpindi", label: "Rawalpindi" },
                { value: "faisalabad", label: "Faisalabad" },
            ],
            sindh: [
                { value: "karachi", label: "Karachi" },
                { value: "hyderabad", label: "Hyderabad" },
            ],
            kpk: [
                { value: "peshawar", label: "Peshawar" },
                { value: "mardan", label: "Mardan" },
            ],
            balochistan: [
                { value: "quetta", label: "Quetta" },
            ],
            gilgit: [
                { value: "gilgit", label: "Gilgit" },
            ],
            ajk: [
                { value: "muzaffarabad", label: "Muzaffarabad" },
            ],
        };

        districtSelect.innerHTML =
            '<option value="">Nothing selected</option>';

        if (!districtsByProvince[province]) return;

        districtsByProvince[province].forEach(function (district) {
            const option = document.createElement("option");
            option.value = district.value;
            option.textContent = district.label;
            districtSelect.appendChild(option);
        });
    }
});

/* =================================
   DEPARTMENT → NOTIFIED SERVICE
================================= */
document.addEventListener("change", function (e) {
    if (e.target && e.target.id === "department_select") {
        const department = e.target.value;
        const notifiedServiceSelect =
            document.getElementById("notified_service_select");

        if (!notifiedServiceSelect) return;

        const servicesByDepartment = {
            health: [
                { value: "hospital_services", label: "Hospital Services" },
                { value: "medical_store", label: "Medical Store Licensing" },
            ],
            education: [
                { value: "school_admission", label: "School Admission" },
                { value: "teacher_transfer", label: "Teacher Transfer" },
            ],
            police: [
                { value: "fir_registration", label: "FIR Registration" },
                { value: "character_certificate", label: "Character Certificate" },
            ],
            local_govt: [
                { value: "birth_certificate", label: "Birth Certificate" },
                { value: "death_certificate", label: "Death Certificate" },
                { value: "sanitation", label: "Sanitation Services" },
            ],
        };

        notifiedServiceSelect.innerHTML =
            '<option value="">Nothing selected</option>';

        if (!servicesByDepartment[department]) return;

        servicesByDepartment[department].forEach(function (service) {
            const option = document.createElement("option");
            option.value = service.value;
            option.textContent = service.label;
            notifiedServiceSelect.appendChild(option);
        });
    }
});
