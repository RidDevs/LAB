const loadData = (callback) => {
    setTimeout(() => {
        const students = [
            { name: "John", marks: 80 },
            { name: "Alice", marks: 90 }
        ];
        console.log("Data Loaded");
        callback(students);
    }, 1000);
};

const processData = (data, callback) => {
    setTimeout(() => {
        const processed = data.map(student => ({
            ...student,
            status: student.marks >= 50 ? "Pass" : "Fail"
        }));
        console.log("Data Processed");
        callback(processed);
    }, 1000);
};

const displayData = (data) => {
    console.log("Processed Data:");
    console.log(data);
};

loadData((data) => {
    processData(data, displayData);
});