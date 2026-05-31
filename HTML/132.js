const loadData = () => {
    return new Promise((resolve) => {
        setTimeout(() => {
            resolve([
                { name: "John", marks: 80 },
                { name: "Alice", marks: 90 }
            ]);
        }, 1000);
    });
};

const processData = (data) => {
    return new Promise((resolve) => {
        setTimeout(() => {
            const processed = data.map(student => ({
                ...student,
                status: student.marks >= 50 ? "Pass" : "Fail"
            }));
            resolve(processed);
        }, 1000);
    });
};

const displayData = (data) => {
    console.log(data);
};

loadData()
    .then(processData)
    .then(displayData)
    .catch(err => console.log(err));